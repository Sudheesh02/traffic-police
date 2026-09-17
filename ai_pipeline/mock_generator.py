"""
Synthetic Test Video and Frame Generator for SynchroClear-ITS Edge-AI Pipeline.

Generates realistic 640x480 surveillance frames simulating Raipur CCTV feeds with:
1. Approaching Emergency Vehicle (Ambulance, Fire Truck, Police Cruiser) or civilian vehicle.
2. Pulsating 1.0 - 2.5 Hz optical strobe beacon (alternating Red / Blue lightbar in upper 25% ROI).
3. High-contrast Indian High Security Registration Plate (HSRP) e.g. CG04MB1234.
4. Roadway environment with stop line and lane markings.

Enables zero-install, zero-weight deterministic offline testing without external dependencies.
"""

import argparse
import math
import os
from pathlib import Path
from typing import Generator, List, Optional, Tuple
import cv2
import numpy as np


# Default scene configuration
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
DEFAULT_FPS = 30.0
DEFAULT_STROBE_HZ = 1.5


def draw_road_background(frame: np.ndarray) -> None:
    """Renders asphalt road, lane delimiters, and stop line."""
    h, w, _ = frame.shape
    # Dark asphalt roadway
    frame[:, :] = (40, 44, 48)

    # Road curbs / sidewalks
    cv2.rectangle(frame, (0, 0), (60, h), (75, 80, 85), -1)
    cv2.rectangle(frame, (w - 60, 0), (w, h), (75, 80, 85), -1)
    cv2.line(frame, (60, 0), (60, h), (180, 180, 180), 2)
    cv2.line(frame, (w - 60, 0), (w - 60, h), (180, 180, 180), 2)

    # Dashed center lane divider
    dash_length = 30
    gap_length = 20
    y = 0
    while y < h:
        cv2.line(frame, (w // 2, y), (w // 2, min(y + dash_length, h)), (240, 240, 240), 3)
        y += dash_length + gap_length

    # Intersection stop line near bottom
    cv2.line(frame, (60, h - 50), (w - 60, h - 50), (250, 250, 250), 6)
    # Yellow warning line 20px behind stop line
    cv2.line(frame, (60, h - 75), (w - 60, h - 75), (20, 210, 240), 2)


def draw_license_plate(
    frame: np.ndarray,
    plate_rect: Tuple[int, int, int, int],
    plate_text: str = "CG04MB1234"
) -> None:
    """
    Renders high-contrast Indian High Security Registration Plate (HSRP).
    Features white background, dark border, IND hologram mark, and bold black characters.
    """
    px, py, pw, ph = plate_rect
    # White reflective plate surface
    cv2.rectangle(frame, (px, py), (px + pw, py + ph), (250, 250, 250), -1)
    # Dark border
    cv2.rectangle(frame, (px, py), (px + pw, py + ph), (10, 10, 10), 2)

    # Blue IND strip on left edge
    ind_w = max(6, pw // 10)
    cv2.rectangle(frame, (px + 1, py + 1), (px + ind_w, py + ph - 1), (180, 50, 20), -1)
    cv2.putText(
        frame, "IND", (px + 2, py + ph - 8),
        cv2.FONT_HERSHEY_PLAIN, 0.6, (255, 255, 255), 1
    )

    # License plate registration string
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 0.65
    thickness = 2
    text_size = cv2.getTextSize(plate_text, font, font_scale, thickness)[0]
    # Center text horizontally in remainder of plate
    text_x = px + ind_w + (pw - ind_w - text_size[0]) // 2
    text_y = py + (ph + text_size[1]) // 2 - 1
    cv2.putText(frame, plate_text, (text_x, text_y), font, font_scale, (10, 10, 10), thickness)


def draw_rooftop_strobe(
    frame: np.ndarray,
    roof_rect: Tuple[int, int, int, int],
    frame_idx: int,
    fps: float = DEFAULT_FPS,
    strobe_hz: float = DEFAULT_STROBE_HZ,
    is_spoof: bool = False
) -> Tuple[bool, bool]:
    """
    Renders rooftop emergency beacon with alternating Red and Blue strobe pulses.
    Calculates exact temporal phase for strobe_hz flash rate.
    Returns (red_active, blue_active).
    """
    rx, ry, rw, rh = roof_rect

    # Dark aerodynamic lightbar bracket
    bar_h = 16
    bar_y = ry + 8
    cv2.rectangle(frame, (rx, bar_y), (rx + rw, bar_y + bar_h), (35, 35, 38), -1)
    cv2.rectangle(frame, (rx, bar_y), (rx + rw, bar_y + bar_h), (80, 80, 85), 1)

    left_center = (rx + rw // 4, bar_y + bar_h // 2)
    right_center = (rx + 3 * rw // 4, bar_y + bar_h // 2)
    strobe_radius = 11

    if is_spoof or strobe_hz <= 0:
        # Spoof ambulance: Static dim lights or no pulse (0 Hz)
        cv2.circle(frame, left_center, strobe_radius, (30, 20, 100), -1)
        cv2.circle(frame, right_center, strobe_radius, (100, 30, 20), -1)
        return False, False

    # Temporal strobe modulation (e.g. 1.5 Hz => period = fps / 1.5 = 20 frames)
    period_frames = max(2, int(round(fps / strobe_hz)))
    cycle_phase = (frame_idx % period_frames) / period_frames

    # Phase 0.0 to 0.5: Red Active (Left), Blue Inactive (Right)
    # Phase 0.5 to 1.0: Blue Active (Right), Red Inactive (Left)
    red_active = cycle_phase < 0.5
    blue_active = not red_active

    if red_active:
        # Glowing Red strobe (Left)
        # Outer soft glow
        cv2.circle(frame, left_center, strobe_radius + 9, (10, 10, 200), -1)
        # Mid halo
        cv2.circle(frame, left_center, strobe_radius + 4, (30, 40, 240), -1)
        # Saturated intense core: High V, High S in HSV
        cv2.circle(frame, left_center, strobe_radius, (15, 20, 255), -1)
        cv2.circle(frame, left_center, 4, (200, 220, 255), -1)

        # Inactive Blue strobe (Right) - dim
        cv2.circle(frame, right_center, strobe_radius, (90, 30, 15), -1)
    else:
        # Inactive Red strobe (Left) - dim
        cv2.circle(frame, left_center, strobe_radius, (15, 20, 90), -1)

        # Glowing Blue strobe (Right)
        # Outer soft glow
        cv2.circle(frame, right_center, strobe_radius + 9, (200, 60, 15), -1)
        # Mid halo
        cv2.circle(frame, right_center, strobe_radius + 4, (240, 110, 30), -1)
        # Saturated intense core: High V, High S in HSV
        cv2.circle(frame, right_center, strobe_radius, (255, 140, 20), -1)
        cv2.circle(frame, right_center, 4, (255, 240, 220), -1)

    return red_active, blue_active


def generate_frame(
    frame_idx: int = 0,
    total_frames: int = 60,
    vehicle_type: str = "AMBULANCE",
    license_plate: str = "CG04MB1234",
    strobe_hz: float = DEFAULT_STROBE_HZ,
    fps: float = DEFAULT_FPS,
    is_spoof: bool = False
) -> np.ndarray:
    """
    Synthesizes a single 640x480 surveillance frame.

    Args:
        frame_idx: Current frame index in sequence (0 to total_frames - 1).
        total_frames: Total length of test clip.
        vehicle_type: "AMBULANCE", "FIRE_TRUCK", "POLICE_CRUISER", or "CIVILIAN_CAR".
        license_plate: Alphanumeric registration string to render on bumper.
        strobe_hz: Flashing frequency of optical beacon in Hz.
        fps: Frame rate for temporal calculations.
        is_spoof: If True, renders vehicle without functional 1.5 Hz strobe.

    Returns:
        np.ndarray: BGR image of shape (480, 640, 3).
    """
    frame = np.zeros((DEFAULT_HEIGHT, DEFAULT_WIDTH, 3), dtype=np.uint8)
    draw_road_background(frame)

    # Vehicle bounding box centered in approach lane
    # (x, y, w, h)
    vx, vy, vw, vh = 180, 120, 280, 270

    if vehicle_type == "AMBULANCE":
        # White chassis
        cv2.rectangle(frame, (vx, vy + 30), (vx + vw, vy + vh), (245, 245, 248), -1)
        cv2.rectangle(frame, (vx, vy + 30), (vx + vw, vy + vh), (160, 160, 165), 2)

        # Windshield / cabin glass
        cv2.rectangle(frame, (vx + 20, vy + 40), (vx + vw - 20, vy + 115), (75, 85, 95), -1)
        cv2.rectangle(frame, (vx + 20, vy + 40), (vx + vw - 20, vy + 115), (35, 45, 55), 2)

        # Emergency Red Stripe across lower middle
        cv2.rectangle(frame, (vx, vy + 145), (vx + vw, vy + 175), (25, 25, 220), -1)

        # Emergency Red Cross emblem (+)
        cross_cx = vx + vw // 2
        cross_cy = vy + 160
        # Horizontal crossbar
        cv2.rectangle(frame, (cross_cx - 24, cross_cy - 7), (cross_cx + 24, cross_cy + 7), (255, 255, 255), -1)
        cv2.rectangle(frame, (cross_cx - 22, cross_cy - 5), (cross_cx + 22, cross_cy + 5), (20, 20, 220), -1)
        # Vertical crossbar
        cv2.rectangle(frame, (cross_cx - 7, cross_cy - 24), (cross_cx + 7, cross_cy + 24), (255, 255, 255), -1)
        cv2.rectangle(frame, (cross_cx - 5, cross_cy - 22), (cross_cx + 5, cross_cy + 22), (20, 20, 220), -1)

        # Headlights
        cv2.circle(frame, (vx + 35, vy + 195), 14, (210, 245, 255), -1)
        cv2.circle(frame, (vx + vw - 35, vy + 195), 14, (210, 245, 255), -1)

        # Front bumper
        cv2.rectangle(frame, (vx + 10, vy + 215), (vx + vw - 10, vy + 265), (55, 58, 62), -1)
        cv2.rectangle(frame, (vx + 10, vy + 215), (vx + vw - 10, vy + 265), (25, 28, 30), 2)

        # License Plate in center of bumper
        plate_w, plate_h = 144, 38
        plate_x = vx + (vw - plate_w) // 2
        plate_y = vy + 222
        draw_license_plate(frame, (plate_x, plate_y, plate_w, plate_h), license_plate)

        # Rooftop Emergency Beacon (Upper 25% ROI: y in [vy, vy + 0.25*vh])
        roof_rect = (vx + 35, vy, vw - 70, int(0.25 * vh))
        draw_rooftop_strobe(frame, roof_rect, frame_idx, fps, strobe_hz, is_spoof)

    elif vehicle_type == "FIRE_TRUCK":
        # Red chassis
        cv2.rectangle(frame, (vx - 10, vy + 20), (vx + vw + 10, vy + vh + 10), (25, 25, 205), -1)
        cv2.rectangle(frame, (vx - 10, vy + 20), (vx + vw + 10, vy + vh + 10), (15, 15, 120), 2)

        # Windshield
        cv2.rectangle(frame, (vx + 15, vy + 35), (vx + vw - 15, vy + 110), (60, 70, 80), -1)

        # White contrast stripe
        cv2.rectangle(frame, (vx - 10, vy + 145), (vx + vw + 10, vy + 175), (240, 240, 240), -1)
        cv2.putText(
            frame, "FIRE RESCUE", (vx + 45, vy + 168),
            cv2.FONT_HERSHEY_DUPLEX, 0.7, (20, 20, 200), 2
        )

        # Bumper & License plate
        cv2.rectangle(frame, (vx, vy + 220), (vx + vw, vy + 275), (45, 45, 50), -1)
        plate_w, plate_h = 144, 38
        plate_x = vx + (vw - plate_w) // 2
        plate_y = vy + 228
        draw_license_plate(frame, (plate_x, plate_y, plate_w, plate_h), license_plate)

        # Rooftop Strobe
        roof_rect = (vx + 25, vy - 10, vw - 50, int(0.25 * vh))
        draw_rooftop_strobe(frame, roof_rect, frame_idx, fps, strobe_hz, is_spoof)

    elif vehicle_type == "POLICE_CRUISER":
        # White & Dark Blue chassis
        cv2.rectangle(frame, (vx, vy + 35), (vx + vw, vy + vh - 20), (240, 240, 240), -1)
        # Blue lower half
        cv2.rectangle(frame, (vx, vy + 130), (vx + vw, vy + vh - 20), (130, 35, 15), -1)

        # Windshield
        cv2.rectangle(frame, (vx + 25, vy + 45), (vx + vw - 25, vy + 115), (70, 80, 90), -1)

        # POLICE emblem text
        cv2.putText(
            frame, "POLICE", (vx + 75, vy + 170),
            cv2.FONT_HERSHEY_DUPLEX, 0.8, (250, 250, 250), 2
        )

        # Bumper & License plate
        cv2.rectangle(frame, (vx + 10, vy + 205), (vx + vw - 10, vy + 248), (40, 40, 42), -1)
        plate_w, plate_h = 144, 38
        plate_x = vx + (vw - plate_w) // 2
        plate_y = vy + 208
        draw_license_plate(frame, (plate_x, plate_y, plate_w, plate_h), license_plate)

        # Rooftop Strobe
        roof_rect = (vx + 35, vy + 5, vw - 70, int(0.25 * vh))
        draw_rooftop_strobe(frame, roof_rect, frame_idx, fps, strobe_hz, is_spoof)

    else:  # CIVILIAN_CAR
        # Silver sedan
        cv2.rectangle(frame, (vx + 20, vy + 45), (vx + vw - 20, vy + vh - 30), (180, 185, 190), -1)
        cv2.rectangle(frame, (vx + 20, vy + 45), (vx + vw - 20, vy + vh - 30), (100, 105, 110), 2)
        cv2.rectangle(frame, (vx + 40, vy + 60), (vx + vw - 40, vy + 120), (60, 70, 80), -1)
        # Bumper & License plate
        cv2.rectangle(frame, (vx + 30, vy + 195), (vx + vw - 30, vy + 235), (50, 50, 55), -1)
        plate_w, plate_h = 144, 38
        plate_x = vx + (vw - plate_w) // 2
        plate_y = vy + 196
        draw_license_plate(frame, (plate_x, plate_y, plate_w, plate_h), license_plate)

    # Frame metadata watermark in upper left
    hud_text = f"CAM: RPR_GE_04 | FPS: {fps:.1f} | F#: {frame_idx:03d} | STROBE: {strobe_hz:.1f}Hz"
    cv2.putText(frame, hud_text, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 200), 1)

    return frame


def generate_sequence(
    num_frames: int = 60,
    fps: float = DEFAULT_FPS,
    vehicle_type: str = "AMBULANCE",
    license_plate: str = "CG04MB1234",
    strobe_hz: float = DEFAULT_STROBE_HZ,
    is_spoof: bool = False
) -> List[np.ndarray]:
    """Generates a list of synthetic video frames."""
    return [
        generate_frame(
            frame_idx=i,
            total_frames=num_frames,
            vehicle_type=vehicle_type,
            license_plate=license_plate,
            strobe_hz=strobe_hz,
            fps=fps,
            is_spoof=is_spoof
        )
        for i in range(num_frames)
    ]


def frame_stream(
    num_frames: int = 60,
    fps: float = DEFAULT_FPS,
    vehicle_type: str = "AMBULANCE",
    license_plate: str = "CG04MB1234",
    strobe_hz: float = DEFAULT_STROBE_HZ,
    is_spoof: bool = False
) -> Generator[np.ndarray, None, None]:
    """Yields synthetic video frames one by one for stream processing."""
    for i in range(num_frames):
        yield generate_frame(
            frame_idx=i,
            total_frames=num_frames,
            vehicle_type=vehicle_type,
            license_plate=license_plate,
            strobe_hz=strobe_hz,
            fps=fps,
            is_spoof=is_spoof
        )


def save_mock_video(
    output_path: str,
    num_frames: int = 60,
    fps: float = DEFAULT_FPS,
    vehicle_type: str = "AMBULANCE",
    license_plate: str = "CG04MB1234",
    strobe_hz: float = DEFAULT_STROBE_HZ,
    is_spoof: bool = False
) -> str:
    """Encodes and saves synthetic frames into an MP4 video file."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (DEFAULT_WIDTH, DEFAULT_HEIGHT))

    for frame in frame_stream(num_frames, fps, vehicle_type, license_plate, strobe_hz, is_spoof):
        writer.write(frame)

    writer.release()
    return output_path


def save_mock_frames(
    output_dir: str,
    num_frames: int = 5,
    vehicle_type: str = "AMBULANCE",
    license_plate: str = "CG04MB1234",
    strobe_hz: float = DEFAULT_STROBE_HZ
) -> List[str]:
    """Saves individual synthetic frames to disk as PNG images."""
    os.makedirs(output_dir, exist_ok=True)
    saved_paths = []
    for i in range(num_frames):
        frame = generate_frame(
            frame_idx=i,
            total_frames=num_frames,
            vehicle_type=vehicle_type,
            license_plate=license_plate,
            strobe_hz=strobe_hz
        )
        file_path = os.path.join(output_dir, f"frame_{i:03d}.png")
        cv2.imwrite(file_path, frame)
        saved_paths.append(file_path)
    return saved_paths


def main() -> None:
    parser = argparse.ArgumentParser(description="SynchroClear-ITS Synthetic Test Video Generator")
    parser.add_argument("--output-dir", type=str, default="ai_pipeline/test_data", help="Directory to save test outputs")
    parser.add_argument("--frames", type=int, default=60, help="Number of frames to generate")
    parser.add_argument("--fps", type=float, default=30.0, help="Simulated frame rate (FPS)")
    parser.add_argument("--vehicle", type=str, default="AMBULANCE", choices=["AMBULANCE", "FIRE_TRUCK", "POLICE_CRUISER", "CIVILIAN_CAR"])
    parser.add_argument("--plate", type=str, default="CG04MB1234", help="Plate text to render")
    parser.add_argument("--strobe-hz", type=float, default=1.5, help="Strobe beacon flash frequency (Hz)")
    parser.add_argument("--save-video", action="store_true", help="Save MP4 video file")
    parser.add_argument("--spoof", action="store_true", help="Generate spoof ambulance (no strobe)")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Save single sample frame
    sample_frame_path = os.path.join(args.output_dir, "sample_ambulance_frame.png")
    frame = generate_frame(0, args.frames, args.vehicle, args.plate, args.strobe_hz, args.fps, args.spoof)
    cv2.imwrite(sample_frame_path, frame)
    print(f"[MockGenerator] Sample frame saved: {sample_frame_path}")

    if args.save_video:
        video_path = os.path.join(args.output_dir, "sample_strobe_sequence.mp4")
        save_mock_video(
            video_path,
            num_frames=args.frames,
            fps=args.fps,
            vehicle_type=args.vehicle,
            license_plate=args.plate,
            strobe_hz=args.strobe_hz,
            is_spoof=args.spoof
        )
        print(f"[MockGenerator] Synthetic video saved: {video_path} ({args.frames} frames @ {args.fps} FPS)")


if __name__ == "__main__":
    main()
