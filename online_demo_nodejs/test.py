# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from alex_asr import Decoder
import wave
import struct
import os


MODEL_PATH = "../vivos_model"


def word_ids_to_str_hyp(decoder, word_ids):
	return" ".join(decoder.get_word(word_id).decode('utf8') for word_id in word_ids)
filename = sys.argv[1]

if __name__ == "__main__":
	decoder = Decoder(MODEL_PATH)

	file_name = os.path.join(os.path.dirname(__file__), "uploads/"+filename)

	data = wave.open(file_name)

	n_decoded = 0
	while True:
		frames = data.readframes(8000)
		if len(frames) == 0:
			break

		decoder.accept_audio(frames)
		n_decoded += decoder.decode(8000)

		if n_decoded > 0:
			prob, word_ids = decoder.get_best_path()
	decoder.input_finished()
	print(word_ids_to_str_hyp(decoder, word_ids))