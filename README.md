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
| tiny_keyword | FALSE 	  | string	| false   | true/false      | If true you can use tiny keywords, these accuracy is slightly lower than the standard model but it consumes considerably less resources |

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
To create your own wake word you have to use the [optimizer from the porcupine repository](https://github.com/Picovoice/Porcupine/tree/master/tools/optimizer). You can only create keywords for Linux, Mac and Windows and in our case we cannot create keywords for the raspberry. 
If you use Kalliope on a x86_64 machine with Linux and want to create your own wake word you do it with the above commands. The wake word Kalliope will be saved in your home directory.
Note, keywords created by the optimizer tool will expire after 90 days.

```yaml
git clone https://github.com/Picovoice/Porcupine.git
cd Porcupine
tools/optimizer/linux/x86_64/pv_porcupine_optimizer -r resources -w "Kalliope" -p linux -o ~/
```

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
