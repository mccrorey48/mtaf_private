var csv = require("fast-csv");

csv
.fromPath("pro_short.csv", {headers: ["name", "domain", "username", "password"]})
.on("data", function(user){
  if (user.name !== "name")
    console.log(user);
})
.on("end", function(){
  console.log("done");
});