import csv
import matplotlib.pyplot as plt



# z_count = 0
# b_count = 0
# eng = 0

years = []
genres = {}
genre_raw = []

with open("./IMDb movies.csv", 'r') as file:

	rows = csv.reader(file)

	first = True
	min_year = 2222

	for row in rows:
		if first:
			first = False
			continue

		# if len(row[13]) < 75:
		# 	z_count += 1
		# 	continue
		# elif len(row[13]) > 250:
		# 	b_count += 1
		# 	continue

		# if row[8] == 'English':
		# 	eng +=1

		# if len(row[13]) > max_size:
		# 	max_size = len(row[13])

		# lengths.append(len(row[13]))

		if row[8] != 'English' or len(row[13]) < 75 or len(row[13]) > 250:
			continue

		curr_genres = row[5].split(", ")

		for g in curr_genres:
			if g in genres:
				genres[g] += 1
			else:
				genres[g] = 1
			genre_raw.append(g)

		# if int(row[3]) < min_year:
		# 	min_year = int(row[3])

		# years.append(int(row[3]))
		# if int(row[3]) in years:
		# 	years[int(row[3])] += 1
		# else: 
		# 	years[int(row[3])] = 1

out_genres = []
counts = []

tups = []

for k in genres:
	if genres[k] > 500:
		counts.append(genres[k])
		out_genres.append(k)

		tups.append((k,genres[k]))

tups.sort(reverse=True, key=lambda tup: tup[1])

out1 = []
out2 = []
for t in tups:
	out1.append(t[0])
	out2.append(t[1])

plt.bar(out1, out2)
# plt.bar(out_genres, counts)
plt.ylabel('Frequency')
plt.xlabel('Genre')
plt.xticks(rotation='vertical')
plt.title("English Language Movies with Descriptions of 75-250 words")
plt.show()



# decade = min_year - (min_year % 10)

# decades = []
# dec_freqs = []

# while decade < 2020:
# 	decades.append(decade)

# 	total = 0
# 	for i in range(9):
# 		if decade+i in years:
# 			total += years[decade+i]

# 	dec_freqs.append(total)

# 	decade += 10
# print(dec_freqs)

# plt.hist(years, decades)
# plt.ylabel('Frequency')
# plt.xlabel('Movie Release Year')
# plt.title("English Language Movies with Descriptions of 75-250 words")
# plt.show()

# freqs = [0]*(max_size+1)

# for length in lengths:
# 	freqs[length] += 1
	

# print('zeros')
# print(z_count)
# print('bigs')
# print(b_count)
# print('USA')
# print(eng)

# plt.plot(freqs[75:])
# plt.ylabel('Frequency')
# plt.xlabel('Length of Movie Description')
# plt.show()