# Pendulum
 ## agent.py	, pendulum_env.py	and  RLGlue.py  from OpenAI: necessary "default notebooks" for this project
 Pendulum environment.The diagram below illustrates the environment.

![](https://miro.medium.com/max/752/1*J_oEx0kpBpwXoVmRytn6qg.gif)
 

The environment consists of single pendulum that can swing 360 degrees. The pendulum is actuated by applying a torque on its pivot point. The goal is to get the pendulum to balance up-right from its resting position (hanging down at the bottom with no velocity) and maintain it as long as possible. The pendulum can move freely, subject only to gravity and the action applied by the agent.

The state is 2-dimensional, which consists of the current angle   and current angular velocity.  
The goal is to swing-up the pendulum and maintain its upright angle. 

Furthermore, since the goal is to reach and maintain a vertical position, there are no terminations nor episodes. Thus this problem can be formulated as a continuing task.

 
