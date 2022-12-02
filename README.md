**Logger** repository splits log file handlers for every test(s) being executed.

- No matter what how many times test module is called in a test run.
- Always generated unique file name and file handler.
- Channelize the log records called from a test module to right file handler.
