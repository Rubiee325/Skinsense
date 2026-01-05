## Models Directory

- `demo_weights/` – Optional small checkpoints for quick local testing (not included by default).
- `checkpoints/` – Training outputs from `train_detector.py` and `train_predictor.py`.

To test the detector end-to-end:

1. Populate `data/demo_detector/train` and `data/demo_detector/val` with a few labeled sample images.
2. Run:

```bash
cd backend
python train_detector.py
```

3. This will create a `detector_mobilenetv3_demo.pt` file under `models/demo_weights/`.
4. The FastAPI app will automatically load this file if present; otherwise, it will use ImageNet-pretrained weights only.






