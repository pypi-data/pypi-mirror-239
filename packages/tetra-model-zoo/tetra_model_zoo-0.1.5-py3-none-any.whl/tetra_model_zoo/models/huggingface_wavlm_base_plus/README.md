[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [HuggingFace-WavLM-Base-Plus: Real-time speech processing.](https://tetra.ai/model-zoo/huggingface_wavlm_base_plus)

HuggingFaceWavLMBasePlus is a real time speech processing backbone based on Microsoft's WavLM model. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of HuggingFace-WavLM-Base-Plus found [here](https://huggingface.co/patrickvonplaten/wavlm-libri-clean-100h-base-plus/tree/main).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/huggingface_wavlm_base_plus


## Example & Usage

Install the package via pip:
```bash
pip install "tetra_model_zoo[huggingface_wavlm_base_plus]"
```

Run the demo:
```bash
python -m tetra_model_zoo.models.huggingface_wavlm_base_plus.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate HuggingFace-WavLM-Base-Plus for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate HuggingFace-WavLM-Base-Plus for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.huggingface_wavlm_base_plus.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using HuggingFace-WavLM-Base-Plus in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of HuggingFace-WavLM-Base-Plus can be found [here](https://github.com/microsoft/unilm/blob/master/LICENSE).


## References
* [WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing](https://arxiv.org/abs/2110.13900)
* [Source Model Implementation](https://huggingface.co/patrickvonplaten/wavlm-libri-clean-100h-base-plus/tree/main)
