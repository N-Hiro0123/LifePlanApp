const getStepClass = (itemState) => {
  switch (itemState) {
    case "completed":
    case "entering":
      return "step step-accent";
    case "unfilled":
    default:
      return "step";
  }
};

export default getStepClass;
