import matplotlib.pyplot as plt
import matplotlib.image as mim
import networkx as nx
import quos
# =======================================================================

def gblk():
    """
    Output: Blank nx graph
    """
    return nx.Graph()
# =======================================================================

def gixy(gbeg, aixy):
    """
    Output: Updated nx graph
    gbeg: nx graph from before
    aixy: Array of arrays of item name str, quop x int, qubit y int
    """
    G = gbeg
    liy = []
    pos = {}
    mnx, mny, mxx, mxy = 0, 0, 0, 0
    for ixy in aixy:
        if ixy[2] not in liy: liy += [ixy[2]]
        if (ixy[1]<mnx): mnx = ixy[1]
        if (ixy[2]<mny): mny = ixy[2]
        if (ixy[1]>mxx): mxx = ixy[1]
        if (ixy[2]>mxy): mxy = ixy[2]
    mnx, mxx = mnx-1, mxx+1
    for y in liy:
        pos.update({str(y)+'b':(mnx,-y)})
        pos.update({str(y)+'e':(mxx,-y)})
        G.add_edge(str(y)+'b', str(y)+'e', weight=1)
    for ixy in aixy:
        img = mim.imread((quos.__file__).replace('__init__.py','icons/' + ixy[0]+'.jpg'))
        x, y = ixy[1], -ixy[2]
        nam = str(ixy[1]*1000000+ixy[2])
        G.add_node(nam, image=img, pos=(x,y))
        pos.update({nam:(x,y)})
        # a = plt.axes([x, y, 0.1, 0.1])
        # a.imshow(img)
        # a.set_aspect('equal')
        # a.axis('off')
    nx.draw(G, pos=pos, with_labels=False)
    plt.show()
# =======================================================================

gixy(gblk(), [['Hadamard',1,1],['PauliX',2,2],['PauliY',3,3],['PauliZ',4,4]])
