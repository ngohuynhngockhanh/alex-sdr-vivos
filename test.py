from alex_asr import Decoder
import wave
import struct
import os


MODEL_PATH = "vivos_model"


def word_ids_to_str_hyp(decoder, word_ids):
    return" ".join(decoder.get_word(word_id).decode('utf8') for word_id in word_ids)


if __name__ == "__main__":
    decoder = Decoder(MODEL_PATH)

    file_name = os.path.join(os.path.dirname(__file__), 'VIVOSSPK46_001.wav')

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
            # ivec = decoder.get_ivector()
            #print('Hypothesis: "%s" (speaker finished speaking: %s)' % (word_ids_to_str_hyp(decoder, word_ids), decoder.endpoint_detected(), ))

    decoder.input_finished()
    #print('Final hypothesis: "%s"' % word_ids_to_str_hyp(decoder, word_ids))
    print(word_ids_to_str_hyp(decoder, word_ids))
    #decoder.finalize_decoding()

    #p, lat = decoder.get_lattice()

    '''print ('Resulting lattice:')
    for state in lat.states:
        print ('  State: %s' % state)
        for arc in state.arcs:
            print ('    %s' % decoder.get_word(arc.ilabel))'''



