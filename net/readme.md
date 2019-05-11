```
1.1 为什么连接的时候是三次握手，关闭的时候却是四次握手？

答：因为当Server端收到Client端的SYN连接请求报文后，可以直接发送SYN+ACK报文。其中ACK报文是用来应答的，SYN报文是用来同步的。但是关闭连接时，当Server端收到FIN报文时，很可能并不会立即关闭SOCKET，所以只能先回复一个ACK报文，告诉Client端，”你发的FIN报文我收到了”。只有等到我Server端所有的报文都发送完了，我才能发送FIN报文，因此不能一起发送。故需要四步握手。
1.2 为什么TIME_WAIT状态需要经过2MSL(最大报文段生存时间)才能返回到CLOSE状态？

MSL（MaximumSegment Lifetime），TCP允许不同的实现可以设置不同的MSL值。第一，保证客户端发送的最后一个ACK报文能够到达服务器，因为这个ACK报文可能丢失，站在服务器的角度看来，我已经发送了FIN+ACK报文请求断开了，客户端还没有给我回应，应该是我发送的请求断开报文它没有收到，于是服务器又会重新发送一次，而客户端就能在这个2MSL时间段内收到这个重传的报文，接着给出回应报文，并且会重启2MSL计时器。第二，防止类似与“三次握手”中提到了的“已经失效的连接请求报文段”出现在本连接中。客户端发送完最后一个确认报文后，在这个2MSL时间中，就可以使本连接持续的时间内所产生的所有报文段都从网络中消失。这样新的连接中不会出现旧连接的请求报文。
1.3 为什么建立连接是三次握手，关闭连接确是四次挥手呢？

建立连接的时候，服务器在LISTEN状态下，收到建立连接请求的SYN报文后，把ACK和SYN放在一个报文里发送给客户端。而关闭连接时，服务器收到对方的FIN报文时，仅仅表示对方不再发送数据了但是还能接收数据，而自己也未必全部数据都发送给对方了，所以己方可以立即关闭，也可以发送一些数据给对方后，再发送FIN报文给对方来表示同意现在关闭连接，因此，己方ACK和FIN一般都会分开发送，从而导致多了一次。
1.4 为什么不能用两次握手进行连接？

答：3次握手完成两个重要的功能，既要双方做好发送数据的准备工作(双方都知道彼此已准备好)，也要允许双方就初始序列号进行协商，这个序列号在握手过程中被发送和确认。现在把三次握手改成仅需要两次握手，死锁是可能发生的。作为例子，考虑计算机S和C之间的通信，假定C给S发送一个连接请求分组，S收到了这个分组，并发送了确认应答分组。按照两次握手的协定，S认为连接已经成功地建立了，可以开始发送数据分组。可是，C在S的应答分组在传输中被丢失的情况下，将不知道S是否已准备好，不知道S建立什么样的序列号，C甚至怀疑S是否收到自己的连接请求分组。在这种情况下，C认为连接还未建立成功，将忽略S发来的任何数据分组，只等待连接确认应答分组。而S在发出的分组超时后，重复发送同样的分组。这样就形成了死锁。
1.5 如果已经建立了连接，但是客户端突然出现故障了怎么办？

TCP还设有一个保活计时器，显然，客户端如果出现故障，服务器不能一直等下去，白白浪费资源。服务器每收到一次客户端的请求后都会重新复位这个计时器，时间通常是设置为2小时，若两小时还没有收到客户端的任何数据，服务器就会发送一个探测报文段，以后每隔75分钟发送一次。若一连发送10个探测报文仍然没反应，服务器就认为客户端出了故障，接着就关闭连接。
1.6 为什么要三次握手？

保证可靠的核心就是双方都需要确认自己发送和接受信息的功能正常,但因为网络环境的不稳定性,这一秒能收发下一秒可能网络核心就发生严重拥塞,所以世界上不存在完全可靠的通信协议.两次握手会怎样?若建立连接只需两次握手，客户端并没有太大的变化，在获得服务端的应答后进入ESTABLISHED状态，即确认自己的发送和接受信息的功能正常.但如果服务端在收到连接请求后就进入ESTABLISHED状态,不能保证客户端能收到自己的信息,此时如果网络拥塞，客户端发送的连接请求迟迟到不了服务端，客户端便超时重发请求，如果服务端正确接收并确认应答，双方便开始通信，通信结束后释放连接。此时，如果那个失效的连接请求抵达了服务端，由于只有两次握手，服务端收到请求就会进入ESTABLISHED状态，等待发送数据或主动发送数据。但此时的客户端早已进入CLOSED状态，服务端将会一直等待下去，这样浪费服务端连接资源。
1.7 为什么要四次挥手？

TCP连接的释放一共需要四步,因此称为『四次挥手』.我们知道,TCP连接是双向的,因此在四次挥手中,前两次挥手用于断开一个方向的连接，后两次挥手用于断开另一方向的连接。第一次挥手:若A认为数据发送完成,则它需要向B发送连接释放请求.该请求只有报文头,头中携带的主要参数为:FIN=1,seq=u.此时,A将进入FIN-WAIT-1状态。1，FIN=1表示该报文段是一个连接释放请求.
2，seq=u,u-1是A向B发送的最后一个字节的序号.

第二次挥手:

B收到连接释放请求后,会通知相应的应用程序,告诉它A向B这个方向的连接已经释放.此时B进入CLOSE-WAIT状态,并向A发送连接释放的应答,其报文头包含:ACK=1,seq=v,ack=u+1.

ACK=1：除TCP连接请求报文段以外,TCP通信过程中所有数据报的ACK都为1，表示应答.

1，seq=v，v-1是B向A发送的最后一个字节的序号.

2，ack=u+1表示希望收到从第u+1个字节开始的报文段,并且已经成功接收了前u个字节.A收到该应答,进入FIN-WAIT-2状态,等待B发送连接释放请求.

第二次挥手完成后，A到B方向的连接已经释放，B不会再接收数据，A也不会再发送数据。但B到A方向的连接仍然存在，B可以继续向A发送数据。

第三次挥手:

当B向A发完所有数据后,向A发送连接释放请求,请求头中包含:
FIN=1,ACK=1,seq=w,ack=u+1.随后B进入LAST-ACK状态.

第四次挥手:

A收到释放请求后,向B发送确认应答,此时A进入TIME-WAIT状态.该状态会持续2MSL时间,若该时间段内没有B的重发请求的话,就进入CLOSED状态,撤销TCB.当B收到确认应答后,也便进入CLOSED状态,撤销TCB。

1.8 为什么TCP客户端最后还要发送一次确认呢？

一句话，主要防止已经失效的连接请求报文突然又传送到了服务器，从而产生错误。如果使用的是两次握手建立连接，假设有这样一种场景，客户端发送了第一个请求连接并且没有丢失，只是因为在网络结点中滞留的时间太长了，由于TCP的客户端迟迟没有收到确认报文，以为服务器没有收到，此时重新向服务器发送这条报文，此后客户端和服务器经过两次握手完成连接，传输数据，然后关闭连接。此时此前滞留的那一次请求连接，网络通畅了到达了服务器，这个报文本该是失效的，但是，两次握手的机制将会让客户端和服务器再次建立连接，这将导致不必要的错误和资源的浪费。如果采用的是三次握手，就算是那一次失效的报文传送过来了，服务端接受到了那条失效报文并且回复了确认报文，但是客户端不会再次发出确认。由于服务器收不到确认，就知道客户端并没有请求连接。
1.9 简述TCP三次握手的过程？

答：在TCP/IP协议中，TCP协议提供可靠的连接服务，采用三次握手建立一个连接。第一次握手：建立连接时，客户端发送syn包(syn=j)到服务器，并进入SYN_SEND状态，等待服务器确认。第二次握手：服务器收到syn包，必须确认客户的SYN（ack=j+1），同时自己也发送一个SYN包（syn=k），即SYN+ACK包，此时服务器进入SYN_RECV状态。第三次握手：客户端收到服务器的SYN＋ACK包，向服务器发送确认包ACK(ack=k+1)，此包发送完毕，客户端和服务器进入ESTABLISHED状态，完成三次握手。完成三次握手，客户端与服务器开始传送数据简版：首先A向B发SYN（同步请求），然后B回复SYN+ACK（同步请求应答），最后A回复ACK确认，这样TCP的一次连接（三次握手）的过程就建立了。三次握手我们先明确两个定义：
1，client为数据发送方

2，server为数据接收方

好，下面进行三次握手的总结：

1，client想要向server发送数据，请求连接。这时client想服务器发送一个数据包，其中同步位（SYN）被置为1，表明client申请TCP连接，序号为j。

2，当server接收到了来自client的数据包时，解析发现同步位为1，便知道client是想要简历TCP连接，于是将当前client的IP、端口之类的加入未连接队列中，并向client回复接受连接请求，想client发送数据包，其中同步位为1，并附带确认位ACK=j+1，表明server已经准备好分配资源了，并向client发起连接请求，请求client为建立TCP连接而分配资源。

3，client向server回复一个ACK，并分配资源建立连接。server收到这个确认时也分配资源进行连接的建立。

那么问题来了为什么需要第三次握手？第三次握手失败了怎么办？三次握手有什么缺陷可以被黑客利用，用来对服务器进行攻击？
怎么防范这种攻击？

接下来进行一一解答。

1.9.1 为什么需要第三次握手？

答：如果没有第三次握手，可能会出现如下情况：如果只有两次握手，那么server收到了client的SYN=1的请求连接数据包之后，便会分配资源并且向client发送一个确认位ACK回复数据包。那么，如果在client与server建立连接的过程中，由于网络不顺畅等原因造成的通信链路中存在着残留数据包，即client向server发送的请求建立连接的数据包由于数据链路的拥塞或者质量不佳导致该连接请求数据包仍然在网络的链路中，这些残留数据包会造成如下危害危害：当client与server建立连接，数据发送完毕并且关闭TCP连接之后，如果链路中的残留数据包才到达server，那么server就会认为client重新发送了一次连接申请，便会回复ACK包并且分配资源。并且一直等待client发送数据，这就会造成server的资源浪费。
1.9.2 第三次握手失败了怎么办？

答：当client与server的第三次握手失败了之后，即client发送至server的确认建立连接报文段未能到达server，server在等待client回复ACK的过程中超时了，那么server会向client发送一个RTS报文段并进入关闭状态，即：并不等待client第三次握手的ACK包重传，直接关闭连接请求，这主要是为了防止泛洪攻击，即坏人伪造许多IP向server发送连接请求，从而将server的未连接队列塞满，浪费server的资源。
1.9.3 三次握手有什么缺陷可以被黑客利用，用来对服务器进行攻击？

答：黑客仿造IP大量的向server发送TCP连接请求报文包，从而将server的半连接队列（上文所说的未连接队列，即server收到连接请求SYN之后将client加入半连接队列中）占满，从而使得server拒绝其他正常的连接请求。即拒绝服务攻击
1.9.4 怎么防范这种攻击？

1，缩短服务器接收客户端SYN报文之后的等待连接时间，即SYNtimeout时间，也就是server接收到SYN报文段，到最后放弃此连接请求的超时时间，将SYNtimeout设置的更低，便可以成倍的减少server的负荷，但是过低的SYNtimeout可能会影响正常的TCP连接的建立，一旦网络不通畅便可能导致client连接请求失败2，SYNcookie + SYN proxy 无缝集成（较好的解决方案）SYNcookie：当server接收到client的SYN之后，不立即分配资源，而是根据client发送过来的SYN包计算出一个cookie值，这个cookie值用来存储server返回给client的SYN+ACK数据包中的初始序列号，当client返回第三次握手的ACK包之后进行校验，如果校验成功则server分配资源，建立连接。SYNproxy代理，作为server与client连接的代理，代替server与client建立三次握手的连接，同时SYNproxy与client建立好了三次握手连接之后，确保是正常的TCP连接，而不是TCP泛洪攻击，那么SYNproxy就与server建立三次握手连接，作为代理（网关？）来连通client与server。（类似VPN了解一下。）
``