from matplotlib import pyplot as plt
import matplotlib.patches as patches

def draw_annotations(image, boxes):
    fig, ax = plt.subplots()
    ax.imshow(image)
    for (x1, y1, x2, y2) in boxes:
        rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1,
                                 linewidth=2, edgecolor='lime', facecolor='none')
        ax.add_patch(rect)
    ax.axis("off")
    return fig
