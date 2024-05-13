const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules");

const ONE_GWEI = 1_000_000_000n;

module.exports = buildModule("LockModule", (m) => {
  const lockedAmount = m.getParameter("lockedAmount", ONE_GWEI);

  const lock = m.contract("AxelrodGame_contrat", [], {
    value: lockedAmount,
  });

  return { lock };
});
