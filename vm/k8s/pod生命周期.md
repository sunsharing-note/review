```
系统中表示pod的条目包含一个表示pod状态的字段，称为“status”。“status”字段本身是一个“PodStatus”类型的对象，其中包含一个“phase”字段，用来表示pod当前所处的生命周期状态。以下是“phase”可能的取值：

Value	Description
Pending	系统已经接受pod实例的创建，但其中所包含容器的一个或者多个image还没有创建成功。Pending包含调度计算与通过网络创建image，所以此phase的时间可能会有点长。
Running	Pod已经被调度到某个node上，pod包含的所有容器已经创建完成，至少有一个容器正常运行或者处于启动与重启动过程。
Succeeded	Pod中的所有容器正常终止，并且不会再次启动。
Failed	Pod中所有容器已终止运行，至少有一个容器非正常结束，比如退出码非零，被系统强制杀死等。
Unknow	无法取得pod状态，一般是网络问题引起。
由以上可知，phase表示的pod状态非常粗略与宽泛。

Pod conditions
PodStatus还包含PodConditions字段，此字段表示pod更详细的状态信息，PodConditions是一个数组，数据中的每个成员包含如下六个字段：

lastProbeTime：表示PodConditions最后一次被探测的时间戳。
latTransitionTime：表示PodConditions​​​​​​​中“status”字段最后一次发生变更的时间戳。
message：人可读的最后一次“status”变更的原因
reason：表示最后一次“status”变更原因的标识，不可读。
status：表示pod状态，可能的值“True”、“False”、“Unknow”。
最后一个字段“type”，有如下五种可能取值：

PodScheduled：Pod已经被高度到某个node。
Ready：Pod已经可以接受请求对外提供服务，此时pod可以被加入到相应service的endpoint中。
Initialized：所有初始化容器已经成功启动。
Unschedulable：Pod无法被调度。
ContainersReady：Pod中所有容器的状态处于“ready”状态。
Container probes 
“探针”是指由kubelet周期性调用的处理程序，实现对容器状态的诊断，探针处理程序的实现有以下三种方式：

ExecAction：在容器内执行的特殊命令，如果退出码为0，则表示容器健康。
TCPSocketAction：检测容器某个端口，如果端口打开则认为正常。
HTTPGetAction：向容器的某个路径发起HTTP GET请求，如果返回应答状态码大于等于200小于400则认为正常。
探针的返回结果有以下三种：

Succees：表示容器通过诊断。
Failed：表示容器没有通过诊断。
Unknown：诊断本身失败，所以对容器的诊断结果未知。
以上是探针处理程序的三种实现方式，从kubernetes对探针结果的操作与反应看，探针分成两类：

livenessProbe：表示容器是否正在运行。如果这种类型的探针诊断失败，则 kubelet杀死容器，然后根据restart policy决定后续处理。如果没有提供此种类型的探针则默认诊断成功。
readinessProbe：指示容器是否能处理请求。如果失败，则将此容器的endpoint从所有包含此endpoint的service中删除。当容器处于启动时的初始化阶段时，此探针的诊断结果为Succees，如果没有提供此类探针，默认诊断结果为Success。
由以上可知，探针由kubelet执行，其结果影响kubelet对容器执行何种操作。

When should you use liveness or readiness probes?
如果容器中运行的程序能够健康自检，当发生问题时程序主动退出、销毁，这种情况无需使用livenessProbe，kubelet能根据restart policy正确处理。如果程序不具备自检功能，那么可以通过livenessProbe检测程序状态，当失败时kubelet杀死容器。同样kubelet根据restart policy决定后续处理。比如restart policy设置成"Always"或者"OnFailure"，则重新启动容器。只是重启，并没有试图去修复问题。

如果打算在某项条件具备之前，不允许pod处理请求，则可以使用readinessProbe。readinessProbe失败并不会像livenessProbe一样删除容器，只是阻止容器处理外部发过来的请求。当readinessProbe成功后，容器就可以正常对外提供服务了。

当删除pod时，无需通过readinessProbe实现drain操作。当删除pod时，pod会进入"unready"状态，不管有没有readinessProbe，这种状态会一直操持到pod被stop。

有关探针的详细使用方法： Configure Liveness and Readiness Probes。

Pod and Container status
Pod状态详细参考：PodStatus​​​​​​​

Container状态详细参考：ContainerState

注意pod状态对container的状态有依赖。

Restart policy
有三种重启策略： Always、OnFailure、Never。Always表示容器无论是正常还是异常退出都重启。Onfailure表示只有在容器异常退出时才重启。Never表示无论容器是正常还是异常退出都不重启。Kubernetes根据算法将重启的时间间隔逐渐拉大，重启成功后重置。单纯从重启策略上看的话，重启策略不关系异常退出原因，也没有也异常修复过程集成，好像没有什么鸟毛的用处。如果容器因为自身原因，比如配置问题启动失败而异常退出，那么重启多少次结果都一样。

Pod lifetime
除非被用户或者某个控制器明确删除，否则pod会一直存在。这条规则的例外情况是处于"Succeeded"或者"Failed"的pod，如果处于此种状态超过一定的时限，比如terminated-pod-gc-threshold的设定值，则会被垃圾回收机制清除。

pod控制器与restart policy的适配：

JOB：适用于一次性任务如批量计算，任务结束后pod会被此类控制器清除。JOB的重启策略只能是"OnFailure"或者"Never"。
ReplicationController, ReplicaSet, or Deployment，此类控制器希望pod一直运行下去，它们的restart policy只能是"always"。
DaemonSet：每个node一个pod，很明显此类控制器的restart policy应该是"always"。

Example states
Pod包含一个容器，容器正常退出.

日志正常完成事件
如果重启策略是：
Always: 重启容器; Pod的phase保持在Running.
OnFailure: Pod的phase变成Succeeded.
Never: Pod的phase变成Succeeded.
容器异常退出

日志失败事件。
如果restart policy是：
Always: 重启容器; Pod的phase保持在Running.
OnFailure: 重启容器；Pod的phase保持在Running.
Never: 不重启容器，Pod的phase变成Failed.
Pod有两个容器，其中一个异常退出：

日志失败事件
如果restart policy是：
Always: 重启异常退出容器，pod的phase是Running.
OnFailure:重启异常退出容器，pod的phase是Running .
Never: 不重启容器，但pod的phase依然是Running.
如果容器1没有运行，容器2异常退出:
日志失败事件
如果restart policy是：
Always: 重启异常退出容器，pod的phase是Running.
OnFailure: 重启异常退出容器，pod的phase是Running.
Never: 不重启容器，但pod的phase变成failed.
pod只有一个容器，容器运行时内存溢出：

容器异常退出
日志OOM事件
如果restart policy是：
Always: 重启异常退出容器，pod的phase是Running（不修复问题，重启有什么用？）.
OnFailure: 重启异常退出容器，pod的phase是Running（不修复问题，重启有什么用？）.
Never: pod的phase变成Failed.
pod在运行时磁盘出问题（由谁发现磁盘出问题？）：

杀死所有容器
日志相应事件
pod的phase变成Failed
如果有相关控制器，则控制器在其它地方创建新实例。
pod运行时node离开集群

Node controller 联系不上node，node的状态变成unknown。
Node controller 将pod的状态设置成Failed。
控制器在其它地方设置副本。

```