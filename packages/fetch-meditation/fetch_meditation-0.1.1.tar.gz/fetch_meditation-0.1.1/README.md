# Fetch Meditation Py

* Python library for reading and parsing daily meditations

### Basic Usage
```py
from fetch_meditation.JFTLanguage import JFTLanguage
from fetch_meditation.JFTSettings import JFTSettings
from fetch_meditation.JFT import JFT

settings = JFTSettings(JFTLanguage.Russian)
jft_instance = JFT.get_instance(settings)
jft_entry = jft_instance.fetch()

print(jft_entry.quote)
```
