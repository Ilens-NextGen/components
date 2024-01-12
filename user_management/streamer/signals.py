from django.dispatch import Signal
finished_frame = Signal(["instance", "sender", "image_byte"])
