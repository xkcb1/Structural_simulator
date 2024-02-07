try:
    from qtconsole import inprocess
    from traitlets.config.loader import Config
except (ImportError, NameError):
    print(
        "The example in `jupyter_console_example.py` requires `qtconsole` to run. Install with `pip install qtconsole` or equivalent."
    )


class JupyterConsoleWidget(inprocess.QtInProcessRichJupyterWidget):
    def __init__(self):
        super().__init__()

        self.kernel_manager = inprocess.QtInProcessKernelManager()
        self.kernel_manager.start_kernel()
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()

    def shutdown_kernel(self):
        self.kernel_client.stop_channels()
        self.kernel_manager.shutdown_kernel()
