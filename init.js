db = connect("mongodb://localhost:27017/ski_planner");

// Insert initial data
db.users.insertMany([
  { username: "nice_user", friends: ["Marie", "Carl"], equipment: {ski: "rossignol"} }
]);