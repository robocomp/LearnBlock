#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#
import math

from genericworker import *
import io
from playsound import playsound
import tensorflow as tf
import numpy as np
from text import text_to_sequence
from util import audio
GreetList = ["hi", "hello", "what's up?"]
ByeList = ["bye", "good bye", "see you soon"]
directory = os.path.join(tempfile.gettempdir(), "tacotron")
import random

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel


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


def find_alignment_endpoint(alignment_shape, ratio):
  return math.ceil(alignment_shape[1] * ratio)

class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map):
        super(SpecificWorker, self).__init__(proxy_map)
        self.timer.timeout.connect(self.compute)
        self.Period = 2000
        self.timer.start(self.Period)
        self.graph, self.sess = load_graph("meta/graph-000256_frz.pb")
        self.wav_output = self.graph.get_tensor_by_name("model/griffinlim/Squeeze:0")
        self.alignment_tensor = self.graph.get_tensor_by_name("model/strided_slice_1:0")
        self.inputs = self.graph.get_tensor_by_name("inputs:0")
        self.input_lengths = self.graph.get_tensor_by_name("input_lengths:0")
        self.hparams = tf.contrib.training.HParams(
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

            # MAILABS trim params
            trim_fft_size=1024,
            trim_hop_size=256,
            trim_top_db=40,

            # Model:
            outputs_per_step=5,
            embedding_dim=512,

            # Training:
            batch_size=32,
            adam_beta1=0.9,
            adam_beta2=0.999,
            initial_learning_rate=0.0015,
            learning_rate_decay_halflife=100000,
            use_cmudict=False,  # Use CMUDict during training to learn pronunciation of ARPAbet phonemes

            # Eval:
            max_iters=200,
            griffin_lim_iters=50,
            power=1.5,  # Power to raise magnitudes to prior to Griffin-Lim
        )

    def __del__(self):
        print('SpecificWorker destructor')

    def setParams(self, params):
        return True

    @QtCore.Slot()
    def compute(self):
        print('SpecificWorker.compute...')
        # computeCODE
        # try:
        #	self.differentialrobot_proxy.setSpeedBase(100, 0)
        # except Ice.Exception, e:
        #	traceback.print_exc()
        #	print e

        # The API of python-innermodel is not exactly the same as the C++ version
        # self.innermodel.updateTransformValues("head_rot_tilt_pose", 0, 0, 0, 1.3, 0, 0)
        # z = librobocomp_qmat.QVec(3,0)
        # r = self.innermodel.transform("rgbd", z, "laser")
        # r.printvector("d")
        # print r[0], r[1], r[2]

        return True

    # =============== Methods for Component Implements ==================# ===================================================================
    
    #
    # say
    #
    def say(self, text):
        global directory
        try:
           os.stat(directory)
        except:
           os.mkdir(directory)
        audio_path = os.path.join(directory, text +".wav")

        if os.path.exists(audio_path):
            audio = text + ".wav"
            print("Audio exists... ", audio)
            os.path.join(directory, audio)
            playsound(audio_path)
        else:
            cleaner_names = [x.strip() for x in self.hparams.cleaners.split(',')]
            seq = text_to_sequence(text, cleaner_names)
            feed_dict = {
                self.inputs: [np.asarray(seq, dtype=np.int32)],
                self.input_lengths: np.asarray([len(seq)], dtype=np.int32)
            }
            wav, alignment = self.sess.run(
                [self.wav_output, self.alignment_tensor],
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

            name = text + ".wav"
            os.path.join(directory, name)
            final_audio = directory + name
            with open(final_audio, "wb") as f:
                f.write(out.getvalue())
            playsound(final_audio)
        pass 


    #
    # sayAlternativeGreet
    #
    def sayAlternativeGreet(self):
        global GreetList
        if list:
            text = random.choice(GreetList)
        else:
            text = "Hello"
        self.say(text)
        pass


    #
    # addGreet
    #
    def addGreet(self, newtext):
        global GreetList
        GreetList.append(newtext)
        pass


    #
    # deleteGreet
    #
    def deleteGreet(self, newtext):
        global GreetList
        if newtext in GreetList:
            GreetList.remove(newtext)
        else:
            self.say("The sentence is not found")
        pass

    #
    # showGreet
    #
    def showGreet(self):
        global GreetList
        for text in GreetList:
            self.say(text)
        self.say("These are the sentences found in the list")
        pass   


    #
    # sayAlternativeBye
    #
    def sayAlternativeBye(self):
        global ByeList
        if list:
            text = random.choice(ByeList)
        else:
            text = "Bye"
        self.say(text)
        pass


    #
    # addBye
    #
    def addBye(self, newtext):
        global ByeList
        ByeList.append(newtext)
        pass


    #
    # deleteBye
    #
    def deleteBye(self, newtext):
        global ByeList
        if newtext in ByeList:
            ByeList.remove(newtext)
        else:
            self.say("The sentence is not found")
        pass  
  

    #
    # showBye
    #
    def showBye(self):
        global ByeList
        for text in ByeList:
            self.say(text)
        self.say("These are the sentences found in the list")
        pass
