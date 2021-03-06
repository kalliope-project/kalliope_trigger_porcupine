# Porcupine trigger
Trigger for Kalliope

## Installation
```bash
kalliope install --git-url https://github.com/kalliope-project/kalliope_trigger_porcupine.git
```

## Parameters

| parameter    | required | type    | default | choices         | comment                                                                                          |
|--------------|----------|---------|---------|-----------------|--------------------------------------------------------------------------------------------------|
| keywords     | TRUE     | string  |         |                 |                                                                                                  |
| ppn_file     | TRUE     | string  |         |                 | Path to the porcupine wake word. The path can be absolute or relative to the brain file          |
| sensitivity  | FALSE    | string  | 0.5     | between 0 and 1 | Increasing the sensitivity value lead to better detection rate, but also higher false alarm rate |
| input_device | FALSE    | integer | default | 				| Select the input device 															   |

## Example settings

```yaml
# This is the trigger engine that will catch your magic work to wake up Kalliope. With porcupine we need different keywords for different platforms. The example use the wake word "porcupine" for the raspberry.

default_trigger: "porcupine"

# Trigger engine configuration
triggers:
  - porcupine:
      keywords:
        - keyword: 
            ppn_file: "trigger/porcupine/porcupine_raspberrypi.ppn"

# To use multiple keywords with different sensitivities
triggers:
  - porcupine:
      keywords:  
        - keyword: 
            ppn_file: "trigger/porcupine/porcupine_raspberrypi.ppn"
            sensitivity: 0.4
        - keyword:
            ppn_file: "trigger/porcupine/blueberry_raspberrypi.ppn"
            sensitivity: 0.3
```


## Available Porcupine keyword

You can find existing keywords [here](https://github.com/Picovoice/Porcupine/tree/master/resources/keyword_files). 
To create your own wake word visit [Picovoice Console](https://console.picovoice.ai/). 
Note: 
You can only create wakewords for Linux x86_64 systems. Raspberry is restricted. 

## Update
This trigger currently supports v1.9 keywords. If there is a new version of keywords, those won't work with this trigger. 

If you want to update this trigger by yourself, you can download the new libs from [here](https://github.com/Picovoice/porcupine/tree/master/lib) and replace the old ones. 
```
Folder and filenames: 
cortex-a53 = armv7l (Raspberry 2,3 and 4 (32Bit))
cortex-a72 = armv8l (Raspberry 4 (64Bit)) 
x86_64 = linux
```
You can also create an issue with a request to properly update the trigger.

## Note

You have to add the path to the trigger folder in your settings.
E.g.:
```
# ---------------------------
# resource directory path
# ---------------------------
resource_directory:
  trigger: "resources/trigger"
  neuron: "resources/neurons"
  stt: "resources/stt"
  tts: "resources/tts"
```
