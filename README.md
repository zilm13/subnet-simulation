### Simulations of network services for subnet building in Ethereum 2.0

#### Why?
While [Discovery V5](https://github.com/ethereum/devp2p/blob/master/discv5/discv5.md) is proposed to be a solution for building subnets, it's mainly a successor of [V4](https://github.com/ethereum/devp2p/blob/master/discv4.md) with improved node information distribution routines. 
As [discv5](https://github.com/ethereum/devp2p/blob/master/discv5/discv5.md) was not specially designed for [Ethereum 2.0](https://github.com/ethereum/eth2.0-specs/), it's not made up to the requirements of Eth2 and it may not be suitable to serve for subnet building.
Currently [Ethereum 2.0](https://github.com/ethereum/eth2.0-specs/) requirements like [creating new subnet every epoch](https://github.com/ethereum/eth2.0-specs/blob/dev/specs/validator/0_beacon-chain-validator.md#lookahead) sounds unachievable from experience with Discovery V4.  
 
The issue already addressed in Ethereum core research, for example, "guess and check" method proposed as an alternative for building subnets, yet it was not tested. 
As an area without deep research to this date, subnet building and proposed solutions should be investigated from the perspective of [Ethereum 2.0](https://github.com/ethereum/eth2.0-specs/) network requirements.

#### So what?
This repo is made to find appropriate solution for [Ethereum 2.0](https://github.com/ethereum/eth2.0-specs/) validators subnet building and find a way to match network requirements. Current candidates for this layer are [discv5 topics](https://github.com/ethereum/devp2p/blob/master/discv5/discv5-theory.md#topic-advertisement) and "guess and check" method.

#### How?
In order to achieve research goals following steps are considered 
- Analyze subnet building [Ethereum 2.0](https://github.com/ethereum/eth2.0-specs/) requirements
- Simulate [discv5 topics](https://github.com/ethereum/devp2p/blob/master/discv5/discv5-theory.md#topic-advertisement)
- Simulate "guess and check"
- Analyze and simulate possible [discv5 attacks](https://github.com/ethereum/devp2p/blob/master/discv5/discv5-rationale.md#security-goals)
- Analyze alternatives candidates for subnet building (private validators network etc.)

#### What's going on now?
- [Discovery V5](https://github.com/ethereum/devp2p/blob/master/discv5/discv5.md) implemenation without topics and network layer [started](discv5) in Python
#### What's expected next?
- Adding network layer simulation with [NS3](https://www.nsnam.org/)

