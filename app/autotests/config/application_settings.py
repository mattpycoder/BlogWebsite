from dataclasses import dataclass


@dataclass
class ApplicationSettings:
    debug_locally: bool = False
    headless: bool = True


application_settings = ApplicationSettings()
