/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'ogilmore', // the auth0 domain prefix
    audience: 'caffeine', // the audience set for the auth0 app
    clientId: 'I0sp9jcudnKrDqGxm533TmZoF5G5QTfN', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
