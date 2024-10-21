import torch
import torch.nn as nn
import torch.nn.functional as F
import piq  # SSIM and PSNR


def perceptual_quality_loss(output, target, alpha=1.0, beta=1.0, gamma=1.0):
    """
    Computes a weighted combination of L1, SSIM, and PSNR losses.

    Parameters:
        output (Tensor): Generated image.
        target (Tensor): Ground truth image.
        alpha (float): Weight for L1 loss.
        beta (float): Weight for SSIM loss.
        gamma (float): Weight for PSNR loss.

    Returns:
        Tensor: Weighted combined loss.
    """
    # L1 Loss (Mean Absolute Error)
    l1_loss = F.l1_loss(output, target)

    # SSIM Loss
    ssim_loss = 1 - piq.ssim(output, target, data_range=1.0)

    # PSNR Loss (lower PSNR corresponds to higher loss)
    psnr_value = piq.psnr(output, target, data_range=1.0)
    psnr_loss = -torch.log(psnr_value + 1e-7)  # Log transform for stability

    # Weighted sum of losses
    combined_loss = (alpha * l1_loss) + (beta * ssim_loss) + (gamma * psnr_loss)

    return combined_loss


def perceptual_quality_loss(output, target, alpha=1.0, beta=1.0, gamma=1.0):
    """
    Computes a weighted combination of L1, SSIM, and PSNR losses.

    Parameters:
        output (Tensor): Generated image.
        target (Tensor): Ground truth image.
        alpha (float): Weight for L1 loss.
        beta (float): Weight for SSIM loss.
        gamma (float): Weight for PSNR loss.

    Returns:
        Tensor: Weighted combined loss.
    """
    # L1 Loss (Mean Absolute Error)
    l1_loss = F.l1_loss(output, target)
    print(f"L1 Loss: {l1_loss.item()}")

    # SSIM Loss
    ssim_loss = 1 - piq.ssim(output, target, data_range=1.0)
    print(f"SSIM Loss: {ssim_loss.item()}")

    # PSNR Loss (lower PSNR corresponds to higher loss)
    psnr_value = piq.psnr(output, target, data_range=1.0)
    print(f"PSNR Value: {psnr_value.item()}")

    psnr_loss = -torch.log(psnr_value + 1e-7)  # Log transform for stability
    print(f"PSNR Loss (Log-transformed): {psnr_loss.item()}")

    # Weighted sum of losses
    combined_loss = (alpha * l1_loss) + (beta * ssim_loss) + (gamma * psnr_loss)
    print(f"Combined Perceptual Quality Loss: {combined_loss.item()}")

    return combined_loss


import torch
import torch.nn.functional as F
import piq  # For SSIM and PSNR


def perceptual_adversarial_loss(
    real_images,
    generated_images,
    real_preds,
    fake_preds,
    alpha=1.0,
    beta=1.0,
    gamma=1.0,
    delta=1.0,
):
    """
    Combines adversarial loss with perceptual losses (L1, SSIM, PSNR) for MRI super-resolution tasks.
    """
    # Adversarial Loss (BCE)
    adversarial_loss_real = F.binary_cross_entropy_with_logits(
        real_preds, torch.ones_like(real_preds)
    )
    adversarial_loss_fake = F.binary_cross_entropy_with_logits(
        fake_preds, torch.zeros_like(fake_preds)
    )
    adversarial_loss = (adversarial_loss_real + adversarial_loss_fake) / 2
    print(f"Adversarial Loss (real + fake): {adversarial_loss.item()}")

    # Perceptual L1 Loss
    l1_loss = F.l1_loss(generated_images, real_images)
    print(f"L1 Loss: {l1_loss.item()}")

    # SSIM Loss (1 - SSIM)
    ssim_loss = 1 - piq.ssim(generated_images, real_images, data_range=1.0)
    print(f"SSIM Loss: {ssim_loss.item()}")

    # PSNR Loss
    psnr_value = piq.psnr(generated_images, real_images, data_range=1.0)
    print(f"PSNR Value: {psnr_value.item()}")

    psnr_loss = -torch.log(psnr_value + 1e-7)
    print(f"PSNR Loss (Log-transformed): {psnr_loss.item()}")

    # Weighted sum of all losses
    combined_loss = (
        (alpha * adversarial_loss)
        + (beta * l1_loss)
        + (gamma * ssim_loss)
        + (delta * psnr_loss)
    )
    print(f"Combined Perceptual Adversarial Loss: {combined_loss.item()}")

    return combined_loss


def total_variation_loss(image):
    # Assuming image of shape [1, height, width]
    if len(image.shape) == 3:
        image = image.unsqueeze(0)
    print(f"Image shape after adding batch dimension (if needed): {image.shape}")

    # Calculate TV loss
    tv_loss_x = torch.sum(torch.abs(image[:, :, :, :-1] - image[:, :, :, 1:]))
    tv_loss_y = torch.sum(torch.abs(image[:, :, :-1, :] - image[:, :, 1:, :]))

    tv_loss = tv_loss_x + tv_loss_y
    print(f"Total Variation Loss: {tv_loss.item()}")

    return tv_loss


def GDNLoss(generated_HR, true_LR, estimated_blur_kernel, lambda_tv):
    """
    Combined loss that includes blur kernel estimation and total variation loss.
    """
    # Blur Kernel Estimation loss
    loss_blur = F.mse_loss(true_LR, estimated_blur_kernel)
    print(f"Blur Kernel Estimation Loss: {loss_blur.item()}")

    # Total Variation Loss for edge preservation in HR reconstruction
    tv_loss = total_variation_loss(generated_HR)
    print(f"Total Variation Loss: {tv_loss}")

    # Combined loss
    total_loss = loss_blur + lambda_tv * tv_loss
    print(f"Combined GDN Loss: {total_loss.item()}")

    return total_loss
