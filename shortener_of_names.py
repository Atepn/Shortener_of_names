import pandas
import numpy

def sort_of_backpack(x_data, backpack_size):
    x_data=[(0, 0)]+x_data
    step_table = [[0]*(backpack_size+1) for i in range(len(x_data))]
    for i in range(1, len(x_data)):
        for j in range(backpack_size+1):
            if j >= x_data[i][0]:
                step_table[i][j] = max(step_table[i-1][j], step_table[i-1][j-x_data[i][0]] + x_data[i][1])
            else:
                step_table[i][j] = step_table[i-1][j]
    ind_of_important = []
    step_size = backpack_size
    for i in range(len(x_data)-1, 0, -1):
        if step_table[i][step_size] != step_table[i-1][step_size]:
            ind_of_important = [i-1]+ind_of_important
            step_size -= x_data[i][0]
    return ind_of_important

def shortener(name_X_data):
    x_data = pandas.read_csv(f'csv/{name_X_data}')
    rate_blocks = ['qwertyuiopasdfghjklzxcvbnm', 'QWERTYUIOPASDFGHJKLZXCVBNM', '1234567890']
    for i in range(len(x_data['title'])):
        sep_ch = ', '
        step_str = x_data['title'][i]
        if sep_ch not in step_str:
            sep_ch = ' '
        list_words = step_str.split(sep_ch)
        if len(list_words) <= 2:
            sep_ch = ' '
        list_words = step_str.split(sep_ch)
        list_rate = []
        for word in list_words:
            score = 1
            for bally, block in enumerate(rate_blocks):
                for ch in block:
                    if ch in word:
                        score += bally+1
                        break
            list_rate.append((len(word), score))
        ind_important_word = sort_of_backpack(list_rate, 100-len(list_words)*len(sep_ch))
        step_str = []
        for ind in ind_important_word:
            step_str.append(list_words[ind])
        x_data['title'][i] = sep_ch.join(step_str)
        print(x_data['title'][i])
    x_data.to_csv('csv/Y_data.csv', index = False)

if __name__ == '__main__':
    shortener('X_data.csv')