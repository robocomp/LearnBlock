import io
import math
import numpy as np
import tensorflow as tf
import sys
from hparams import hparams, hparams_debug_string
from librosa import effects
from models import create_model
from text import text_to_sequence
from util import audio


def find_alignment_endpoint(alignment_shape, ratio):
  return math.ceil(alignment_shape[1] * ratio)


class Synthesizer:
  def load(self, checkpoint_path, model_name='tacotron'):
    print('Constructing model: %s' % model_name)
    inputs = tf.placeholder(tf.int32, [1, None], 'inputs')
    input_lengths = tf.placeholder(tf.int32, [1], 'input_lengths')
    with tf.variable_scope('model') as scope:
      self.model = create_model(model_name, hparams)
      self.model.initialize(inputs, input_lengths)
      self.wav_output = audio.inv_spectrogram_tensorflow(
          self.model.linear_outputs[0])
      self.alignment = self.model.alignments[0]

    print('Loading checkpoint: %s' % checkpoint_path)
    self.session = tf.Session()
    self.session.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    saver.restore(self.session, checkpoint_path)

  def synthesize(self, text, return_wav=False):
    cleaner_names = [x.strip() for x in hparams.cleaners.split(',')]
    seq = text_to_sequence(text, cleaner_names)
    feed_dict = {
        self.model.inputs: [np.asarray(seq, dtype=np.int32)],
        self.model.input_lengths: np.asarray([len(seq)], dtype=np.int32)
    }
    wav, alignment = self.session.run(
        [self.wav_output, self.alignment],
        feed_dict=feed_dict
    )

    audio_endpoint = audio.find_endpoint(wav)
    alignment_endpoint = find_alignment_endpoint(
        alignment.shape, audio_endpoint / len(wav)
    )

    wav = wav[:audio_endpoint]
    alignment = alignment[:, :alignment_endpoint]

    if return_wav:
      return wav, alignment

    out = io.BytesIO()
    audio.save_wav(wav, out)
    return out.getvalue(), alignment

  def export(self):
    tf.train.write_graph(tf.compat.v1.graph_util.convert_variables_to_constants(self.session, self.session.graph_def, ["model/griffinlim/Squeeze",'model/strided_slice_1']),'.','{}-{:06d}_frz.pb'.format('graph', 256),as_text=False)

if __name__ == '__main__':
  c = Synthesizer()   
  c.load(sys.argv[1])
  c.export()

