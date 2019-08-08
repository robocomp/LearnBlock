import io
from playsound import playsound
import tensorflow as tf
import numpy as np
from synthesizer import find_alignment_endpoint
from text import text_to_sequence
from util import audio


def load_graph(graph_path):
    graph = tf.Graph()
    with graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(graph_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    sess = tf.Session(graph=graph)
    return graph, sess

hparams = tf.contrib.training.HParams(
    # Comma-separated list of cleaners to run on text prior to training and eval. For non-English
    # text, you may want to use "basic_cleaners" or "transliteration_cleaners" See TRAINING_DATA.md.
    cleaners='english_cleaners',

    # Audio:
    num_mels=80,
    num_freq=1025,
    min_mel_freq=125,
    max_mel_freq=7600,
    sample_rate=22000,
    frame_length_ms=50,
    frame_shift_ms=12.5,
    min_level_db=-100,
    ref_level_db=20,

    #MAILABS trim params
    trim_fft_size=1024,
    trim_hop_size=256,
    trim_top_db=40,

    # Model:
    # TODO: add more configurable hparams
    outputs_per_step=5,
    embedding_dim=512,

    # Training:
    batch_size=32,
    adam_beta1=0.9,
    adam_beta2=0.999,
    initial_learning_rate=0.0015,
    learning_rate_decay_halflife=100000,
    use_cmudict=False,   # Use CMUDict during training to learn pronunciation of ARPAbet phonemes

    # Eval:
    max_iters=200,
    griffin_lim_iters=50,
    power=1.5,              # Power to raise magnitudes to prior to Griffin-Lim
)

if __name__ == '__main__':
    graph, sess = load_graph('graph-000256_frz.pb')
    wav_output = graph.get_tensor_by_name("model/griffinlim/Squeeze:0")
    alignment_tensor = graph.get_tensor_by_name("model/strided_slice_1:0")
    inputs = graph.get_tensor_by_name("inputs:0")
    input_lengths = graph.get_tensor_by_name("input_lengths:0")

    text="Hello Dami, how are you?"

    cleaner_names = [x.strip() for x in hparams.cleaners.split(',')]
    seq = text_to_sequence(text, cleaner_names)
    feed_dict = {
        inputs: [np.asarray(seq, dtype=np.int32)],
        input_lengths: np.asarray([len(seq)], dtype=np.int32)
    }
    wav, alignment = sess.run(
        [wav_output, alignment_tensor],
        feed_dict=feed_dict
    )

    audio_endpoint = audio.find_endpoint(wav)
    alignment_endpoint = find_alignment_endpoint(
        alignment.shape, audio_endpoint / len(wav)
    )

    wav = wav[:audio_endpoint]
    alignment = alignment[:, :alignment_endpoint]


    out = io.BytesIO()
    audio.save_wav(wav, out)

    with open("prueba_hello2.wav", 'wb') as f:
        f.write(out.getvalue())
   # pygame.init()
   # pygame.mixer.init()
   # sound = pygame.mixer.Sound("prueba_hello2.wav")
   # sound.set_volume(0.9)   # Now plays at 90% of full volume.
   # sound.play()
    playsound('prueba_hello2.wav')

