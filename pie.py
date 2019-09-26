import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg
import numpy as np



def generate_inner_colors(no_of_test): #generate no_of_test * 2 dintinct value one for pass and fail for each request

    arr = ['g', 'r'] * no_of_test
    """
    for i  in range(no_of_test):
        arr.append(1 + 4 * i)
        arr.append(2 + 4 * i)
    """
    #print(arr)
    return arr



def generate_labels(dic):
    pass_ratio = np.array(list(map(lambda x : dic[x][0] / (dic[x][0] + dic[x][1]), dic)))
    pass_ratio = np.round(pass_ratio, decimals = 2) * 100
    fail_ratio = 100 - pass_ratio

    req_lis = list(map(lambda x : x, dic))
    labels = []
    for i in range(len(req_lis)):
        labels.append( req_lis[i] + ' pass : ' + str(pass_ratio[i]))
        labels.append( req_lis[i] + ' fail : ' + str(fail_ratio[i]))

    return labels, req_lis


#input : result = {'login': [1, 1], 'getUserInfo': [2, 4], 'updation': [7, 3]} and collection name
#dictionary in format of request name : pass and fail count
def main(result, collection_name):
    #print(result)

    fig, ax = plt.subplots()


    no_of_test = len(result.keys())

    size = 0.3
    vals = np.array(list(map(lambda x : result[x] , result))).astype(float) #for grouping the resuts

    labels, req_lis = generate_labels(result)

    cmap = plt.get_cmap("tab20c")
    inner_colors = cmap(np.arange(no_of_test) )    #generate color for outer ring
    outer_colors = np.array(generate_inner_colors(no_of_test))
    #print(np.arange(no_of_test)*4)
    #print(outer_colors)
    #draw inner cricle for requests
    ax.pie(vals.sum(axis=1), radius=1-size, colors=inner_colors,
           wedgeprops=dict(width=size, edgecolor='w'))

    #draw outer circle wrt pass and fail ratio of indivisual circle
    wedges, texts = ax.pie(vals.flatten(), radius=1, colors=outer_colors,
           wedgeprops=dict(width=size, edgecolor='w'))


    #for labeling sucess
    sucess_bbox_props = dict(boxstyle="square,pad=0.3", fc="g", ec="k", lw=0.72)
    sucess_kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=sucess_bbox_props, zorder=0, va="center")

    #for lebeling fail
    fail_bbox_props = dict(boxstyle="square,pad=0.3", fc="r", ec="k", lw=0.72)
    fail_kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=fail_bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        if i % 2 == 0:
            sucess_kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **sucess_kw)
        else:
            fail_kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **fail_kw)
        #print(i)

    plt.text(0.5, 0.5, 'result', horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)

    ax.set(aspect=1.1,adjustable='box', title='')
    plt.savefig( 'chart.jpg', bbox_inches='tight')


    plt.show()

    #plt.show()
