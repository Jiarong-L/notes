<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global' 
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>


<style>
img{
    width: 60%;
}
</style>


参考：[EasyRL - 蘑菇书](https://datawhalechina.github.io/easy-rl/)，CS285旧笔记（见文件夹）

练习工具：[Gymnasium](https://gymnasium.org.cn/introduction/basic_usage/) 为一些常见的强化学习项目提供环境反馈


## 符号表

at timestep *t*  

$s_t$ - state     
$o_t$ - observation   
$a_t$ - action   
$\pi_\theta(a_t|o_t)$ - policy (partially observed)  
$\pi_\theta(a_t|s_t)$ - policy (fully observed)      
$\tau$ - Trajectory，试验得到的一系列($s_t$,$a_t$)组合  
$H_t$ - History，试验得到的一系列($s_t$,$a_t$,$r_t$)组合


## Ch1 基本知识

强化学习（Reinforcement Learning）的训练目标是：让智能体(Agent)的行为在不确定的环境中最大化奖励（Reward），其困难在于奖励的获取有延迟 / 权衡探索与利用（牺牲一部分短期奖励）

探索(exploration)指尝试不同的新动作对奖励进行**预估**、而不是当前最优的动作，利用(exploitation)指**采取**当前预计最优的动作、但这个预计实际上可能并不准确。由于总步数有限，想要累计奖励最大，需要平衡二者的次数。

RL的常见思路是，如果环境未知，先**学习**环境的运作规则（即下文中 Agent's Model，环境会返回什么新状态）,然后利用这个模型进行**规划**（对策略进行优化）

------------------------------------

一个RL训练样本是一个试验的历史轨迹($\tau$)，是一组时间序列，这有别于普通的监督学习（iid）

在一个试验(Trial)/一个回合(Episode)中，每一步$t$运行一次Agent（依照策略进行一次动作、Env返回新状态），直到游戏结束/超出预定步数

行为(action)可以是离散的（上下左右）也可以是连续的（分子某个亚基左旋多少度）

------------------------------------

**Agent 的组成 (at $s_t$)**

- Policy：依据当前状态选取动作
    - 随机/概率分布 $\pi(a|s)$ 即 $p(a_t = a | s_t = s)$
    - 确定/最优 $\mathop{\arg\min}\limits_{a} \pi(a|s)$ 

- Value Function：对未来累计奖励 $G_t = \sum\limits_{k=0}^{\infty} \gamma^{k} r_{t+k+1}$ 的预测
    - $V_{\pi}(s) = E_{\pi}[G_t | s_t = s] = \sum\limits_{a} \pi(a|s) Q_{\pi}(s,a)$
    - $Q_{\pi}(s,a) = E_{\pi}[G_t | s_t = s, a_t = a]$

- Model：施加选定的动作后，返回新状态 $s'$、奖励
    - 状态转移概率 $p_{ss'}^{a} = p(s_{t+1} = s' | s_t=s, a_t=a)$
    - 奖励 $R(s,a) = E[r_{t+1} | s_t=s, a_t=a ]$

Model-based 需要对环境建模、以预测反馈（需要已知的状态转移函数$P(s_{t+1}|s_{t},a_{t})$，e.g.一些游戏空间），但更多深度学习的情况是 Model-free、即直接从真实环境中获取反馈（e.g.自动驾驶上路训练），可能会有一些采样的问题（采样了s1路线的反馈，但模型跑在未知的s2路线上）

------------------------------------

Value-based Agent 会评估每一对(状态-动作)的价值，选择能带来最高价值的动作；间接获得**确定/最优**的策略，适合离散小空间中的穷举，例如：Q-Learning: $\pi(s) = argmax_a Q(s, a)$）

Policy-based Agent 直接学习策略的**概率分布** $\pi_{\theta}(a|s)$，可以借助价值方程训练策略分布的参数 $\theta$, 以最大化期望总回报，例如：Actor-Critic方法中，Actor根据策略概率抽选动作，Critic评估价值


## Ch2 Markov

本节简写：$s_{t+1}$ -> $s'$, $s_{t}$ -> $s$

------------------------------------

假设，我们定义一个有限状态空间为 $S = (sn_1,sn_2,sn_3,sn_4) $，转移概率矩阵为 $P \text{ where } p_{ij} = P(s_{t+1} = sn_j | s_{t} = sn_{i})$ 的马尔可夫过程。

随机游走一次，可以得到一组具有马尔可夫性质的随机变量序列 $s_1, ..., s_t$，下一刻的状态$s_{t+1}$只取决于当前状态$s_{t}$。

马尔可夫**奖励**过程(Markov reward process, MRP)：为状态空间设定奖励函数 $R = (r_1,r_2,r_3,r_4)$，以上轨迹就有了实际回报，状态 $s \in S$ 的价值 $V(S_i) = E[G_t | s_t = S_i]$ 可推导为**贝尔曼方程** $V(s) = R(s) + \gamma \sum\limits_{s' \in S} p(s' | s)V(s')$    

可以写成矩阵的形式 $V = R + \gamma PV$，解析解 $V = (I -  \gamma P)^{-1}R$ 复杂度为 $O(N^3)$，状态很多时求逆非常困难，需要以迭代的方式求近似（类似 Model-free 的情形）

------------------------------------

MRP游走时之间按照转移概率函数 $p(s_{t+1}| s_{t})$ 进行跳转（不会给智能体偏向的action更多权重）。马尔可夫**决策**过程(MDP)的随机游走中加了一步策略选择 $\pi(a|s) = p(a_t = a | s_t = s)$，于是状态转移按照 $p(s_{t+1}| s_{t},a_{t})$，奖励函数也修改为 $R(s_t,a_t)$

Q函数的**贝尔曼（期望）方程** $Q(s,a) = R(s,a) + \gamma \sum\limits_{s' \in S} p(s' | s，a)V(s')$，其中 $V(s') = \sum\limits_{a' \in A} \pi(a'|s') Q_{\pi}(s',a')$ 是未来状态的期望价值。如果将 $V(s')$ 替换为 $V(s')^{\star} = \max\limits_{a' \in A} Q^{\star}(s',a')$，这就是**贝尔曼（最优）方程**

```bash
贝尔曼期望方程 ---  当前价值 = 即时奖励 + 未来状态的期望折扣价值（所有action的加权均值）
贝尔曼最优方程 ---  当前价值 = 即时奖励 + 未来状态的最佳折扣价值（不再求平均，而是选价值最大的action）
```

MDP的**预测**过程（评估一个给定的策略）：迭代T=k次后收敛（矩阵相乘k次），策略 $\pi$ 的评估基于此时的 $V(s)$，也写作 $V_{\pi}^T(s)$  

```bash
动态规划（DP）:贝尔曼方程可以被拆解成递归的形式 T+1 的值取决于 T 
  - 同步备份（为下一轮生成新表）：每一次迭代都会更新所有状态的值
  - 异步备份（In-place）：可以只更新少量状态
```

MDP的**控制**过程（搜索最佳策略）：迭代（评估、优化）各种不同策略，择出最优 $\pi(s)^{\star} = \argmax\limits_{\pi} V_{\pi}(s)$，即 $a = \argmax\limits_{a \in A} Q^{\star}(s,a)$ 时 $\pi(a|s)^{\star} = 1$


```bash
策略迭代：(上文)
  1. 策略评估：迭代求解贝尔曼(期望)方程，计算当前策略下的状态价值函数 V(s)
  2. 策略优化：基于 V(s)，生成一个"更贪婪"的新策略 π(a|s)，即对状态 s 采用使得 argmax Q(s,a) 的 Action

价值迭代：
  1. 策略评估：迭代求解贝尔曼(最优)方程，直接得到理论最优的价值函数 V(s)*
  2. 策略优化：基于 V(s)*，生成一个"更贪婪"的新策略 ...（同上）
```


------------------------------------









