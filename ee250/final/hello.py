
import numpy as np
import pydub
from pydub import AudioSegment
import os
import sys

print("Just wanna tell you that the script is running!") # DELETE WHEN FINISHED

MAX_FRQ = 30000
SLICE_SIZE = 0.15 #seconds
WINDOW_SIZE = 0.25 #seconds

# TODO: implement this dictionary
specific_dict = {'E4': 330, 'B3': 247, 'G3': 196, 'D3': 147, 'A2': 110, 'E2': 83}
range_dict = {'E4': (321, 339), 'B3': (240, 254), 'G3': (191, 201), 'D3': (143, 151), 'A2': (107, 113), 'E2': (81, 84)}
# LOWER_FRQS = [697, 770, 852, 941]
# HIGHER_FRQS = [1209, 1336, 1477]
# FRQ_THRES = 20



def get_max_frq(frq, fft):
    max_frq = 0
    max_fft = 0
    for idx in range(len(fft)):
        if abs(fft[idx]) > max_fft:
            max_fft = abs(fft[idx])
            max_frq = frq[idx]
    return max_frq

def decoder(average_frequency, target_note): # parameter types: (int, string)
    freq_range = range_dict[target_note]
    text_file = open("result.txt", "w")


    if (average_frequency >= freq_range[0]) and (average_frequency <= freq_range[1]):
        print("You're all set!")
        text_file.write("You're all set!")
    elif average_frequency < freq_range[0]:
        print("Your frequency is too low, which means you gotta tighten the string")
        print("You're at " + str(average_frequency) + "Hz, you should be in this range: " + str(freq_range[0]) + " to "
              + str(freq_range[1]) + "Hz.")
        text_file.write("Your frequency is too low, which means you gotta tighten the string. ")
        text_file.write("You're at " + str(average_frequency) + "Hz, you should be in this range: " + str(freq_range[0]) + " to "
              + str(freq_range[1]) + "Hz.")
    else:
        print("Your frequency is too high, which means you gotta loosen the string")
        print("You're at " + str(average_frequency) + "Hz, you should be in this range: " + str(freq_range[0]) + " to "
              + str(freq_range[1]) + "Hz.")
        text_file.write("Your frequency is too high, which means you gotta loosen the string. ")
        text_file.write("You're at " + str(average_frequency) + "Hz, you should be in this range: " + str(freq_range[0]) + " to "
              + str(freq_range[1]) + "Hz.")
    text_file.close()


def main(file, target_note):
    print("Importing {}".format(file))
    audio = AudioSegment.from_wav(file)

    sample_count = audio.frame_count()
    sample_rate = audio.frame_rate
    samples = audio.get_array_of_samples()

    print("Number of channels: " + str(audio.channels))
    print("Sample count: " + str(sample_count))
    print("Sample rate: " + str(sample_rate))
    print("Sample width: " + str(audio.sample_width))

    slice_sample_size = int(SLICE_SIZE * sample_rate)  # get the number of elements expected for [SLICE_SIZE] seconds

    n = slice_sample_size  # n is the number of elements in the slice

    # generating the frequency spectrum
    k = np.arange(n)  # k is an array from 0 to [n] with a step of 1
    slice_duration = n / sample_rate  # slice_duration is the length of time the sample slice is (seconds)
    frq = k / slice_duration  # generate the frequencies by dividing every element of k by slice_duration

    max_frq_idx = int(MAX_FRQ * slice_duration)  # get the index of the maximum frequency (2000)
    frq = frq[range(max_frq_idx)]  # truncate the frequency array so it goes from 0 to 2000 Hz

    start_index = 0  # set the starting index at 0
    end_index = start_index + slice_sample_size  # find the ending index for the slice
    output = ''

    print()
    i = 1

    result_list = []

    while end_index < len(samples):
        print("Sample {}:".format(i))
        i += 1

        #TODO: grab the sample slice and perform FFT on it

        sample_slice = samples[start_index: end_index]  # take a slice from the samples array for the given start and end index
        sample_slice_fft = np.fft.fft(sample_slice) / n  # perform the fourier transform on the sample_slice and normalize by dividing by n

        #TODO: truncate the FFT to 0 to 1000 Hz
        sample_slice_fft = sample_slice_fft[range(max_frq_idx)]
        sample_slice_fft = np.absolute(sample_slice_fft)

        #TODO: calculate the locations of the upper and lower FFT peak using get_peak_frqs()
        actual_frequency = get_max_frq(frq,sample_slice_fft)
        #TODO: print the values and find the number that corresponds to the numbers
        print("The frequency of this sample segment is: " + str(actual_frequency) + "Hz")

        #Incrementing the start and end window for FFT analysis
        start_index += int(WINDOW_SIZE*sample_rate)
        end_index = start_index + slice_sample_size

        # Registering this result into the list
        result_list.append(int(actual_frequency))

    average_freq = int(sum(result_list) / len(result_list))
    print("Average frequency from samples: " + str(average_freq))
    decoder(average_freq, target_note)


if __name__ == '__main__':
    while True:
        if len(sys.argv) != 2 or not os.path.isfile('output.wav'): # If the user didn't provide target note or the wav file
            # is missing, then we cannot execute the program.
            if len(sys.argv) != 2:
                print("Usage: decode.py [target note]")
                exit(1)

        else:
            print("Let's see if this audio really is note: " + str(sys.argv[1]))
            main('output.wav', str(sys.argv[1]))
            os.remove("output.wav")
            exit(0)
