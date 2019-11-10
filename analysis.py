import xlrd
from sklearn.metrics import cohen_kappa_score
import matplotlib.pyplot as plt
import operator
import numpy as np



def read_file(file, sheetname):
	"""read excel file and save annotations in nested list"""
	sheet = xlrd.open_workbook(file).sheet_by_name(sheetname)
	rowcount = sheet.nrows #Get number of rows 
	colcount = sheet.ncols #Get number of columns
	#write data from excel into list (result is nested list)
	result_data =[]
	for curr_row in range(1, rowcount, 1):
	    row_data = []
	    for curr_col in range(1, colcount-1, 1):
	        data = sheet.cell_value(curr_row, curr_col) # Read the data in the current cell
	        row_data.append(data)
	    result_data.append(row_data)

	#delete irrelevant info at the beginning of file from list
	for l in result_data:
		i = result_data.index(l)
		if i <= 6:
			result_data.pop(0)

	return result_data




def convert_annotations(data_list):
	"""returns dict of sentences with annotated emotion and intensity"""
	annotations = {}
	emotions = ("Anger", "Fear", "Joy", "Surprise", "Sadness", "Disgust")

	for l in data_list:	#for annotated sentence in list
		#save info in dict
		sentence = l[-1]
		for anno in l[:6]:
			if anno[0] is not "0":
				index = l.index(anno)
				emotion = emotions[index]
				intensity = anno
		annotations[sentence] = (emotion, intensity)

	return annotations



def annotation_labels(anno_dict):
	"""returns annotations as nested list: [[emotions], [intensities]]"""
	emotions = []
	intensities = []
	for k,v in anno_dict.items():
		emotions.append(v[0])
		intensities.append(v[1])

	labels = [emotions, intensities]

	return labels




def emotion_count(anno_dict):
	#counts how often emotions were annotated
	emotion_count = {"Anger": 0, "Fear": 0, "Joy": 0, "Surprise": 0, "Sadness": 0, "Disgust": 0}
	for k,v in anno_dict.items():
		emotion = v[0]
		emotion_count[emotion] += 1

	#get number of annotated sentences
	number_annotations = 0
	for k,v in emotion_count.items():
		number_annotations += v
	print("You annotated %s sentences with an emotion." %number_annotations)

	print(emotion_count)
	return emotion_count




def all_stats(anno_dict):
	#counts which intensity was annotated how often for each emotion
	emotion_stats = {"Anger": {"3 High Intentensity": 0, "2 Normal Intensity": 0, "1 Low Intensity": 0},
						"Fear": {"3 High Intentensity": 0, "2 Normal Intensity": 0, "1 Low Intensity": 0},
						"Joy": {"3 High Intentensity": 0, "2 Normal Intensity": 0, "1 Low Intensity": 0},
						"Surprise": {"3 High Intentensity": 0, "2 Normal Intensity": 0, "1 Low Intensity": 0},
						"Sadness": {"3 High Intentensity": 0, "2 Normal Intensity": 0, "1 Low Intensity": 0},
						"Disgust": {"3 High Intentensity": 0, "2 Normal Intensity": 0, "1 Low Intensity": 0}}

	for k,v in anno_dict.items():
		emotion = v[0]
		intensity = v[1]
		emotion_stats[emotion][intensity] += 1

	print(emotion_stats)
	return emotion_stats




def annotator_agreement(anno1, anno2):
	"""calculates inter-annotator agreement with cohen's kappa"""
	A1 = anno1[0]
	A2 = anno2[0]
	kappa = cohen_kappa_score(A1, A2, labels=None, sample_weight=None)

	print("The inter-annotator agreement k = %s." %round(kappa, 2))
	return kappa




def disagreements(anno_dict1, anno_dict2):
	"""returns sentences that were annotated differently"""
	differences = {}

	for k,v in anno_dict1.items():
		label1 = v[0]
		label2 = anno_dict2[k][0]
		if label1 != label2:
			differences[k] = (label1, label2)

	print(differences)
	return differences



def vis_freq_emotions(emo_count1, emo_count2):
	"""makes bar plot for annotated emotions and there frequencies,
	for each annotation """
	n_groups = len(emo_count2)
	#sort annotations biggest value
	sorted_dict1 = sorted(emo_count1.items(), key=operator.itemgetter(1))
	sorted_dict1.reverse()
	sorted_dict2 = sorted(emo_count2.items(), key=operator.itemgetter(1))
	sorted_dict2.reverse()

	#save emotions and freqs in list by same index
	emotions1, emotions2 = [], []
	freqs1, freqs2 = [], []

	for n in sorted_dict1:
		emotions1.append(n[0])
		freqs1.append(n[1])

	for n in sorted_dict2:
		freqs2.append(n[1])

	#plot emotions-frequencies for both annotations
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.35
	opacity = 0.8

	rects1 = plt.bar(index, freqs1, bar_width,
	alpha=opacity, color='b', label='Annotation 1')

	rects2 = plt.bar(index + bar_width, freqs2, bar_width,
	alpha=opacity, color='g', label='Annotation 2')

	plt.ylabel('Absolute Occurrences')
	plt.title('Absolute occurrences of emotion for each annotation')
	plt.xticks(index + bar_width, emotions1)
	plt.legend()

	plt.tight_layout()
	plt.show()




if __name__ == '__main__':
	file1 = "EmotionAnalysis-Annotation1.xlsx"
	file2 = "EmotionAnalysis-Annotation2.xlsx"
	sheet = "V2 Example Annotation Environme"

	data1 = read_file(file1, sheet)
	data2 = read_file(file2, sheet)

	annotations1 = convert_annotations(data1)
	annotations2 = convert_annotations(data2)

	emotion1 = emotion_count(annotations1)
	emotion2 = emotion_count(annotations2)

	labels1 = annotation_labels(annotations1)
	labels2 = annotation_labels(annotations2)

	annotator_agreement(labels1, labels2)

	#print(emotion1)
	#print(emotion2)

	#print(annotations1)
	#print(annotations2)

	disagreements(annotations1, annotations2)

	vis_freq_emotions(emotion1, emotion2)


	





