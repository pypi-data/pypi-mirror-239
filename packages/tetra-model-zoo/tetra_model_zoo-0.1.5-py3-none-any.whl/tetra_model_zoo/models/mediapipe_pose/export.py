from __future__ import annotations

from typing import Any, Tuple

import torch

import tetra_hub as hub
from tetra_model_zoo.models._shared.mediapipe.utils import trace_mediapipe
from tetra_model_zoo.models.mediapipe_pose.model import MediaPipePose
from tetra_model_zoo.utils.args import base_export_parser
from tetra_model_zoo.utils.hub import download_hub_models


def trace(
    pose_detector: torch.nn.Module, landmark_detector: torch.nn.Module
) -> Tuple[Any, Any]:
    """
    Convert the models to pytorch traces. Traces can be saved & loaded from disk.
    With Tetra Hub, a pytorch trace can be exported to run efficiently on mobile devices!

    Inputs:
        pose_detector
            Pose detector model, from load_mediapipe_pose_models()
        pose_landmark_detector
            Pose landmark detector model, from load_mediapipe_pose_models()

    Returns: Tuple[Pose Detector Trace Object, Landmark Detector Trace Object]
    """
    return trace_mediapipe(
        MediaPipePose.get_pose_detector_input_spec(),
        pose_detector,
        MediaPipePose.get_pose_landmark_detector_input_spec(1),
        landmark_detector,
    )


def main():
    # Export parameters
    parser = base_export_parser()
    args = parser.parse_args()

    # Load source models
    model = MediaPipePose.from_pretrained()
    pose_detector = model.pose_detector
    pose_landmark = model.pose_landmark_detector

    # Trace the model.
    traced_encoder, traced_decoder = trace(pose_detector, pose_landmark)  # type: ignore

    # Select the device you'd like to optimize for.
    devices = [hub.Device(device) for device in args.devices]

    # Submit the traced models for conversion & profiling.
    box_detector_jobs = hub.submit_profile_job(
        name="pose_detector",
        model=traced_encoder,
        input_shapes=MediaPipePose.get_pose_detector_input_spec(),
        device=devices,
    )

    landmark_detector_jobs = hub.submit_profile_job(
        name="pose_landmark_detector",
        model=traced_decoder,
        input_shapes=MediaPipePose.get_pose_landmark_detector_input_spec(1),
        device=devices,
    )

    # Download the optimized assets!
    print("Exported pose detector(s):\n")
    download_hub_models(box_detector_jobs)
    print("Exported pose landmark detector(s):\n")
    download_hub_models(landmark_detector_jobs)


if __name__ == "__main__":
    main()
