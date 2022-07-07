const express = require('express')
const app = express()
const port = 3002

app.use(express.static(__dirname + '/client'));
app.get("/globe", (req, res) => {
  res.sendFile(__dirname + "/client/sphere.html");
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
