const getStepClass = (itemState) => {
  switch (itemState) {
    case "completed":
    case "entering":
      return "step step-primary";
    case "unfilled":
    default:
      return "step";
  }
};

export default getStepClass;
