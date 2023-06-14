img{
    width: 30%;
}
</style>



2D、3D结构之间的转换，操作详情见 [RDKit_Doc](http://www.rdkit.org/docs/GettingStartedInPython.html)；**ToDo：复习化学后更新此页面**。


### 结构文件
* 1D(Smiles .smi)
* 2D(MDL mol .mol)
* 3D(sdf mol2)

### 获得1D/2D结构
* [Swiss ADME](http://www.swissadme.ch/)
* [Corina Online](https://demos.mn-am.com/corina_interactive.html)
* PubChem 下载
* ZINC 下载


### MolFromXX
此外：SmilesMolSupplier(smi), SDMolSupplier(sdf)
```
from rdkit import Chem
from rdkit.Chem import AllChem
import nglview


m = Chem.MolFromSmarts('Cc1ccccc1')              ## 2D
_m = Chem.MolFromSmiles('C[C@H](O)c1ccccc1')     ## 2D
_m = Chem.MolFromPDBFile('pdb/1oky.pdb')         ## 3D
_m = Chem.MolFromFASTA('>aa\nTCGATCGATCGATCGA\n',flavor=7)   ## 2D & MMFFOptimize Fail
_m = Chem.MolFromSequence('KKVKKVKKV',flavor=1)              ## 2D & MMFFOptimize Fail



m = Chem.AddHs(m)                            ## 补全H        
AllChem.EmbedMolecule(m, randomSeed=3)       ## 通过距离几何算法计算3D坐标
AllChem.MMFFOptimizeMolecule(m)              ## 力场优化


_ = AllChem.EmbedMultipleConfs(m, useExpTorsionAnglePrefs=True, useBasicKnowledge=True)
view = nglview.show_rdkit(m)
view
```

MolFromSequence/MolFromFASTA 
```
        - flavor: (optional)
            - 0 Protein, L amino acids (default)
            - 1 Protein, D amino acids
            - 2 RNA, no cap
            - 3 RNA, 5' cap
            - 4 RNA, 3' cap
            - 5 RNA, both caps
            - 6 DNA, no cap
            - 7 DNA, 5' cap
            - 8 DNA, 3' cap
            - 9 DNA, both caps
```
![1](RDKit/img/1.png) ![2](RDKit/img/2.png)

### MolToXX
与MolFromXX反一反
```
Chem.MolToSmiles(m)
Chem.MolToSmarts(m)
Chem.MolToFASTA(m)
Chem.MolToSequence(m)


Chem.Draw.MolToImage(m)
```


### Edit
Some: 
```
m = Chem.Kekulize(m)                 ## 清除芳香环信息，但输出smile后再返回会恢复该信息

tt = Chem.MolFromSmiles('OC')
ss = Chem.MolFromSmarts('[$(NC(=O))]')
m = Chem.MolFromSmiles('CC(=O)N')
m = AllChem.ReplaceSubstructs(m,ss,tt)


m = Chem.MolFromSmiles('BrCCc1cncnc1C(=O)O')
core = Chem.MolFromSmiles('c1cncnc1')
m = Chem.ReplaceSidechains(m,core)   ## m = Chem.ReplaceCore(m,core)



m = Chem.MolFromSmiles('CC(=O)C=CC=C')
mw = Chem.RWMol(m)
mw.ReplaceAtom(4,Chem.Atom(7))
mw.AddAtom(Chem.Atom(6))
mw.AddBond(6,7,Chem.BondType.SINGLE)
mw.RemoveAtom(0)
```



## 参考
**RDKit**: http://www.rdkit.org/docs/GettingStartedInPython.html  


