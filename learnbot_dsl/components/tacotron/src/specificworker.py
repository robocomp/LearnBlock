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
import tempfile
from text import text_to_sequence
from util import audio
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
        # English graph
        graph, sess = load_graph("meta/graph-000256_frz.pb")
        wav_output = graph.get_tensor_by_name("model/griffinlim/Squeeze:0")
        alignment_tensor = graph.get_tensor_by_name("model/strided_slice_1:0")
        inputs = graph.get_tensor_by_name("inputs:0")
        input_lengths = graph.get_tensor_by_name("input_lengths:0")
        self.tts = {"en": (graph, sess, wav_output, alignment_tensor, inputs, input_lengths, 'english_cleaners')}
        
        # Spanish Graph
        # graph, sess = load_graph("meta/spanish.pb")
        # wav_output = self.graph.get_tensor_by_name("model/griffinlim/Squeeze:0")
        # alignment_tensor = self.graph.get_tensor_by_name("model/strided_slice_1:0")
        # inputs = self.graph.get_tensor_by_name("inputs:0")
        # input_lengths = self.graph.get_tensor_by_name("input_lengths:0")
        # self.tts["es"] = (graph, sess, wav_output, alignment_tensor, inputs, input_lengths, 'english_cleaners')

        self.alternatives_greetings = {"es": ["hola", "¿qué tal?", "hey"], "en": ["hi", "hello", "what's up?"]}
        self.alternatives_farewells = {"es": ["adios", "hasta pronto", "hasta la proxima"], "en": ["bye", "good bye", "see you soon"]}

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
    # This method synthesizes the text and reproduces the audio generated in the language passed by parameters
    #
    def say(self, text, language):
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
            if language.lower() in self.tts:
                graph, sess, wav_output, alignment_tensor, inputs, input_lengths, cleaners = self.tts[language.lower()]
                cleaner_names = [x.strip() for x in cleaners]
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

                name = text + ".wav"
                os.path.join(directory, name)
                final_audio = directory + name
                with open(final_audio, "wb") as f:
                    f.write(out.getvalue())
                playsound(final_audio)
        pass 


    #
    # This method chooses a random greeting in the chosen language and is sent to the say() method to generate an audio.
    #
    def sayAlternativeGreet(self, language):
        if language.lower() in self.alternatives_greetings:
            text = random.choice(self.alternatives_greetings[language])
        else:
            text = "No greeting sentences available in that language"
        self.say(text, language)
        pass


    #
    # This method adds a greeting to the dictionary of greetings in the selected language.
    #
    def addGreet(self, newtext, language):
        if language.lower() in self.alternatives_greetings: 
            self.alternatives_greetings[language.lower()].append[newtext]
        else:
            self.say("No greeting sentences available in that language")
        pass


    #
    # This method eliminates a greeting to the dictionary of greetings in the selected language.
    #
    def deleteGreet(self, newtext, language):
        if newtext in alternatives_greetings[language.lower()] and language.lower() in self.alternatives_greetings:
            self.alternatives_greetings[language.lower()].remove(newtext)
        else:
            self.say("The sentence is not found in that language")
        pass

    #
    # This method shows all available phrases in the greetings dictionary in the selected language.
    #
    def showGreet(self, language):
        if language.lower() in self.alternatives_greetings.values():
            for text in self.alternatives_greeting[language]:
                self.alternatives_greeting[language].say(text)
        else:
            self.say("No greeting sentences available in that language")
        pass   


    #
    # This method chooses a random farewell in the chosen language and is sent to the say() method to generate an audio.
    #
    def sayAlternativeBye(self, language):
        if language.lower() in self.alternatives_farewells:
            text = random.choice(self.alternatives_farewells[language])
        else:
            text = "No farewell sentences available in that language"
        self.say(text)
        pass


    #
    # This method adds a farewell to the dictionary of farewells in the selected language.
    #
    def addBye(self, newtext, language):
        if language.lower() in self.alternatives_farewells:
            self.alternatives_farewells[language].append(newtext)
        else:
            self.say("No farewell sentences available in that language")
        pass


    #
    # This method eliminates a farewell to the dictionary of farewells in the selected language.
    #
    def deleteBye(self, newtext, language):
        if newtext in self.alternatives_farewells[language.lower()] and language.lower() in self.alternatives_farewells:
            self.alternatives_farewells[language.lower()].remove(newtext)
        else:
            self.say("The sentence is not found in that language")
        pass  
  

    #
    # This method shows all available phrases in the farewell dictionary in the selected language.
    #
    def showBye(self, language):
        if language.lower() in self.alternatives_farewells:
            for text in self.alternatives_farewells[language.lower()]:
                self.alternatives_lower[language.lower()].say(text)
        else:
            self.say("No farewell sentences available in that language")
        pass
