"""
File: babygraphics.py
Name: Kang
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt',
    'data/full/baby-2020.txt'
]
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010, 2020]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    split_space = (width-GRAPH_MARGIN_SIZE*2) / len(YEARS)
    x_coordinate = GRAPH_MARGIN_SIZE + year_index*split_space

    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #
    bleed = GRAPH_MARGIN_SIZE
    width = CANVAS_WIDTH
    height = CANVAS_HEIGHT
    for i in range(len(YEARS)):
        x_coordinate = get_x_coordinate(width, i)
        canvas.create_line(x_coordinate, 0, x_coordinate, height)
        canvas.create_text(x_coordinate+TEXT_DX, height-bleed, text=YEARS[i], anchor='nw')

    canvas.create_line(bleed, bleed, width-bleed, bleed)
    canvas.create_line(bleed, height-bleed, width-bleed, height-bleed)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #
    lookup_names_count = 0
    for name in lookup_names:  #
        color_variable = lookup_names_count % 4
        lookup_names_count += 1
        for i in range(len(YEARS)-1):

            x1 = get_x_coordinate(CANVAS_WIDTH, i)  # x1 = 年代線的x
            x2 = get_x_coordinate(CANVAS_WIDTH, i+1)  # x2 = 下一個年代線的x

            if str(YEARS[i]) not in name_data[name]:  # 如果name在YEAR[i]中沒有排名，就設定y1在最低點。YEAR[i]是int
                y1 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE  # 所以要把int轉成str，才能對應到name_data中尋找
                rank = '*'  # 如果沒有排名就以“＊”代替

                if str(YEARS[i+1]) not in name_data[name]:  # 如果name在YEAR[i+1]中沒有排名，就設定y2在最低點
                    y2 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                else:
                    y2 = int(name_data[name][str(YEARS[i + 1])])*CANVAS_HEIGHT/MAX_RANK  # 不然就依排名為y2*0.6 有可能超過螢幕高度

            else:  # 如果name在YEAR[i]中有排名，就設定排名為y1*0.6
                y1 = int(name_data[name][str(YEARS[i])])*CANVAS_HEIGHT/MAX_RANK
                y2 = int(name_data[name][str(YEARS[i + 1])])*CANVAS_HEIGHT/MAX_RANK
                rank = name_data[name][str(YEARS[i])]  # # 如果有排名就代入

                if int(y1) > CANVAS_HEIGHT:  # 如果該年排名大於螢幕高度，就以最低名次帶入
                    y1 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                    rank = '*'
                    if int(y2) > CANVAS_HEIGHT:  # 如果次年排名也大於螢幕也以最低名次帶入
                        y2 = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                        rank = '*'

                elif int(y1) < GRAPH_MARGIN_SIZE:  # 如果該年排名小於表的留白，以最低名次帶入
                    y1 = GRAPH_MARGIN_SIZE
                    rank = int(name_data[name][str(YEARS[i])])
                    if int(y2) < GRAPH_MARGIN_SIZE:
                        y2 = GRAPH_MARGIN_SIZE

                elif int(y2) < GRAPH_MARGIN_SIZE:  # 如果次年排名也小於表的留白，也以最低名次帶入
                    y2 = GRAPH_MARGIN_SIZE

            text = name + ' ' + str(rank)
            canvas.create_line(x1, y1, x2, y2, fill=COLORS[color_variable], width=LINE_WIDTH)
            canvas.create_text(x1 + TEXT_DX, y1, text=text, anchor='sw', fill=COLORS[color_variable])

            if i == len(YEARS)-1:
                rank = name_data[name][str(YEARS[i])]
                text = name + ' ' + str(rank)
                canvas.create_text(x2 + TEXT_DX, y2, text=text, anchor='sw', fill=COLORS[color_variable])


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
