import express from 'express';
import { createProxyServer } from 'http-proxy';

const app = express();
const proxy = createProxyServer({});

app.use('/conversations', (req, res) => {
  proxy.web(req, res, { target: 'http://logicrasacbsvr.southindia.cloudapp.azure.com:5005' });
});

app.listen(3000, () => {
  console.log('Proxy server listening on port 3000');
});
