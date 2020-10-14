# Import NeMo and ASR collection
import nemo
import nemo.collections.asr as nemo_asr
try:
    nf = nemo.core.NeuralModuleFactory()
except:
    print("GPU was not detected. Running on CPU")
    nf = nemo.core.NeuralModuleFactory(placement=nemo.core.DeviceType.CPU)




NEMO_GIT_ROOT='../nemo-repo'
#First, load the config from YAML file
from ruamel.yaml import YAML
yaml = YAML(typ="safe")
with open(NEMO_GIT_ROOT+"/examples/asr/conf/quartznet_15x5.yaml") as file:
    model_definition = yaml.load(file)




# List all available models from NGC
for checkpoint in nemo.collections.asr.models.ASRConvCTCModel.list_pretrained_models():
    print(checkpoint.pretrained_model_name)




# Automagically go to NGC and instantiate a model and weights
quartznet_model4 = nemo_asr.models.QuartzNet.from_pretrained(model_info="QuartzNet15x5-En")
print(f"Created QuartzNet model with {quartznet_model4.num_weights} weights")





# Change these to point to your training data
train_manifest = "manifests/ls_train_100.json"
val_manifest = "manifests/ls_test.json"
print(model_definition)
labels = model_definition['model']['labels']
data_layer = nemo_asr.AudioToTextDataLayer(manifest_filepath=train_manifest, labels=labels, batch_size=16)
data_layerE = nemo_asr.AudioToTextDataLayer(manifest_filepath=val_manifest, labels=labels, batch_size=16)
ctc_loss = nemo_asr.CTCLossNM(num_classes=len(labels))
greedy_decoder = nemo_asr.GreedyCTCDecoder()

audio_signal, audio_signal_len, transcript, transcript_len = data_layer()
log_probs, encoded_len = quartznet_model4(input_signal=audio_signal, length=audio_signal_len)
predictions = greedy_decoder(log_probs=log_probs)
loss = ctc_loss(log_probs=log_probs, targets=transcript,
                input_length=encoded_len, target_length=transcript_len)

# START TRAINING 
tensors_to_evaluate=[predictions, transcript, transcript_len]
from functools import partial
from nemo.collections.asr.helpers import monitor_asr_train_progress
train_callback = nemo.core.SimpleLossLoggerCallback(
    tensors=[loss]+tensors_to_evaluate,
    print_func=partial(monitor_asr_train_progress, labels=labels))
nf.train(tensors_to_optimize=[loss],
                callbacks=[train_callback],
                optimizer="novograd",
                optimization_params={"num_epochs": 1, "lr": 1e-2,
                                    "weight_decay": 1e-3})
