const { ethers, network } = require("hardhat");
const { expect } = require("chai");

describe("[AnotherPlease Exploit]", function () {
  let deployer, user1, challenge, exploit;

  before(async function () {
    [user1, deployer] = await ethers.getSigners();

    if (network.name == "hardhat") {
      const Challenge = await ethers.getContractFactory(
        "AnotherPlease",
        deployer
      );
      challenge = await Challenge.deploy();
    } else {
      challenge = await ethers.getContractAt(
        "AnotherPlease",
        "0x8c6d48B34E92155cC06733d2699232582Af4b65F"
      );
    }
  });

  it("exploit", async function () {
    const Exploit = await ethers.getContractFactory(
      "AnotherPleaseExploit",
      user1
    );
    exploit = await Exploit.deploy(challenge.address);
    await exploit.exploit();
    expect(await challenge.balanceOf(exploit.address)).to.equal(30);
  });

  it("Sanity Check", async function () {
    await exploit.sendIt();
    expect(await challenge.balanceOf(user1.address)).to.equal(30);
  });
});
