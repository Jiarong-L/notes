<style>
img{
    width: 30%;
}
</style>

**jupyter notebook 中**展示3D分子结构（交互式）。懒人代码： [NGLView.ipynb](NGLView/NGLView.ipynb)  



### load mol
```
import nglview
from rdkit import Chem
from rdkit.Chem import AllChem

m = Chem.MolFromFASTA('>aa\nTCGA\n',flavor=7)

AllChem.EmbedMolecule(m, randomSeed=3)       ## 通过距离几何算法计算3D坐标
AllChem.MMFFOptimizeMolecule(m)              ## 力场优化

_ = AllChem.EmbedMultipleConfs(m, useExpTorsionAnglePrefs=True, useBasicKnowledge=True)
view = nglview.show_rdkit(m)
view
```
![TCGA](NGLView/img/1.png)

### load pdb
```
import nglview

view = nglview.show_file('http://www.rcsb.org/pdb/files/1oky.pdb')  ## or local
view = nglview.show_pdbid('1oky')

view                   ## can rotate/zoom
```
![PDB](NGLView/img/2.png)



## 参考
**nglview**: http://nglviewer.org/nglview/latest/api.html

