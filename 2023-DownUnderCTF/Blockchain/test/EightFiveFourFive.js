const { ethers, network } = require("hardhat");
const { expect } = require("chai");

describe("[EighFiveFourFive Exploit]", function () {
  let deployer, user1, challenge;

  before(async function () {
    [user1, deployer] = await ethers.getSigners();

    if (network.name == "hardhat") {
      const Challenge = await ethers.getContractFactory(
        "EightFiveFourFive",
        deployer
      );
      challenge = await Challenge.deploy("str_to_solve");
    } else {
      challenge = await ethers.getContractAt(
        "EightFiveFourFive",
        "0xf22cB0Ca047e88AC996c17683Cee290518093574"
      );
    }
  });

  it("exploit", async function () {
    let str = await challenge.connect(user1).readTheStringHere();
    await challenge.connect(user1).solve_the_challenge(str);
  });

  it("Sanity Check", async function () {
    expect(await challenge.connect(user1).isSolved()).to.equal(true);
  });
});
