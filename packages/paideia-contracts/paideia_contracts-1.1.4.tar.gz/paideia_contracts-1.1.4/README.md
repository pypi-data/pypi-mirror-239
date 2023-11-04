# paideia-contracts

Paideia ErgoScript smart-contracts. 

# Details

This repository contains the ErgoScript smart-contracts used within the Paideia project, along with their respective EIP-6 protocol specifications.

# Python Library

This repository can also be installed as a python library and used within your own project:

`pip install paideia-contracts`

# Overall Architecture

![Paideia Architecture](paideia_contracts/img/Paideia%20-%20Paideia%20Architecture.jpg)

Paideia consists of a number of interacting modules.

## Paideia

The origin of all DAO's that use Paideia lies in the Paideia module, ensuring the DAO's that are created are verified and living up to the requirements. DAO's created through the Paideia module will get official tokens during the creation process to proof Paideia was used to create the DAO

## DAO

Once the DAO is created the DAO module is the core of following modules. The treasury is handled here and any underlying modules need to be created in accordance with this module to be a verified part of the DAO. For example a configuration box to be used in smart contracts (either standard Paideia contracts or contracts made by the DAO itself) can proof its validity with a token distributed by the DAO module.

## Profit sharing

If the DAO uses profit sharing this will hook into the staking module so profits are automatically distributed to stakers.

## Staking

The staking system will be similar to the existing staking setup, enhanced with extra rewards from the profit sharing module and will be key to the voting setup

## Proposals

Proposals can be initiated by DAO members and have 1 or more actions related to them that will be performed if the proposal passes. A proposal can have different types of voting and will depend on settings stored in a config box. For example a config could be the % quorum needed for a proposal to pass. The total amount of possible votes is determined by using the Staking module (total amount staked).

## Voting

A DAO member can participate in voting by creating a voting box with their stake key. The stake key will be stored in the vote box and instead the member will receive a vote key. This vote key can be used to vote on active proposals. The stake box belonging to the stake key will be used as a data input to determine voting power. When a vote is cast the proposal is updated accordingly and the vote box stores the proposal ID voted on to prevent double voting. By storing these ID's in a collection it will be possible to vote on multiple overlapping proposals. The stake key can only be retrieved if the vote box is not involved in any active proposals (withdrawing a vote could potentially be a DAO config).

## Action
An action is something that happens if a proposal passes. This could something as simple as sending an amount of erg to an address, changing a config or updating a smart contract to a new version.

## Config
One or more config boxes can be in use by a DAO and can act as oracles for the smart contracts in use by the DAO. Standard Paideia related config will always be present, but if needed the DAO can create a new config box with an action.

# Contracts

- [Staking Protocol](paideia_contracts/contracts/staking/README.md)