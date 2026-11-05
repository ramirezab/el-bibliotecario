"""El modelo local: Stable Diffusion XL + pixel-art-xl + ControlNet de bordes, en la tarjeta de video.

Parte del dibujo a color de Forja (img2img): los colores y las formas ya están puestos, el modelo solo los repinta
en pixel art. Así la capucha es verde en todos los ángulos porque ya era verde, y de espaldas no aparece una cara
porque en el dibujo no la hay. Los bordes (ControlNet) sostienen la silueta.

Memoria: la descripción de cada vista se codifica una sola vez al cargar y los dos codificadores de texto se
sueltan. El resto (UNet, ControlNet, VAE: ~5,6 GB) vive en la tarjeta de video, no en la RAM.
"""
import gc

import torch

BASE = 'stabilityai/stable-diffusion-xl-base-1.0'
VAE = 'madebyollin/sdxl-vae-fp16-fix'
CONTROL = 'diffusers/controlnet-canny-sdxl-1.0-small'
LORA = ('nerijs/pixel-art-xl', 'pixel-art-xl.safetensors')

NEGATIVO = ('blurry, smooth shading, gradient, 3d render, realistic, photo, text, watermark, signature, '
            'extra limbs, extra arms, deformed hands, cropped, frame, border, multiple characters, scenery, wall, floor')

# (palabras de la vista, lo que no debe aparecer en esa vista)
VISTAS = {
    'frente': ('front view', ''),
    'tres_cuartos': ('three-quarter view', ''),
    'lado': ('side view, profile', ''),
    'tres_cuartos_atras': ('back three-quarter view, seen from behind', 'face, eyes'),
    'atras': ('back view, seen from behind, back of the hood', 'face, eyes, mouth'),
}


def vista(yaw):
    """Qué vista es, según el giro respecto a la cámara (yaw 0 = de frente)."""
    y = yaw % 360
    d = min(y, 360 - y)
    if d < 25:
        return 'frente'
    if d < 70:
        return 'tres_cuartos'
    if d < 115:
        return 'lado'
    if d < 160:
        return 'tres_cuartos_atras'
    return 'atras'


class Motor:
    def __init__(self, descripcion, fuerza_lora=1.0):
        from diffusers import (AutoencoderKL, ControlNetModel, EulerDiscreteScheduler,
                               StableDiffusionXLControlNetImg2ImgPipeline)
        cn = ControlNetModel.from_pretrained(CONTROL, torch_dtype=torch.float16)
        vae = AutoencoderKL.from_pretrained(VAE, torch_dtype=torch.float16)
        pipe = StableDiffusionXLControlNetImg2ImgPipeline.from_pretrained(
            BASE, controlnet=cn, vae=vae, torch_dtype=torch.float16, variant='fp16', use_safetensors=True)
        pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
        pipe.load_lora_weights(LORA[0], weight_name=LORA[1], adapter_name='pixel')
        pipe.set_adapters(['pixel'], adapter_weights=[fuerza_lora])

        # 1) los textos de todas las vistas, de una vez
        pipe.text_encoder.to('cuda')
        pipe.text_encoder_2.to('cuda')
        self.textos = {}
        with torch.no_grad():
            for clave, (palabras, sin) in VISTAS.items():
                pe, npe, ppe, nppe = pipe.encode_prompt(
                    prompt=f'pixel art, {descripcion}, {palabras}, full body, plain white background',
                    device='cuda', num_images_per_prompt=1, do_classifier_free_guidance=True,
                    negative_prompt=NEGATIVO + (', ' + sin if sin else ''))
                self.textos[clave] = dict(prompt_embeds=pe, negative_prompt_embeds=npe,
                                          pooled_prompt_embeds=ppe, negative_pooled_prompt_embeds=nppe)
        # 2) se sueltan los codificadores de texto
        pipe.text_encoder = None
        pipe.text_encoder_2 = None
        gc.collect()
        torch.cuda.empty_cache()
        # 3) lo demás a la tarjeta de video
        pipe.unet.to('cuda')
        pipe.controlnet.to('cuda')
        pipe.vae.to('cuda')
        if hasattr(pipe.vae, 'enable_tiling'):
            pipe.vae.enable_tiling()
        gc.collect()
        self.pipe = pipe

    def pintar(self, base, bordes, yaw=0, semilla=7, pasos=30, guia=6.0, control=0.6, fuerza=0.55):
        """`base`: el dibujo de Forja sobre fondo liso (RGB). `fuerza`: cuánto puede cambiarlo (0 = nada, 1 = todo)."""
        g = torch.Generator('cpu').manual_seed(semilla)
        with torch.no_grad():
            im = self.pipe(image=base, control_image=bordes, strength=fuerza, **self.textos[vista(yaw)],
                           num_inference_steps=pasos, guidance_scale=guia, controlnet_conditioning_scale=control,
                           generator=g, width=base.width, height=base.height).images[0]
        torch.cuda.empty_cache()
        return im
