/* Exercise shipped error presentation without a browser or another dependency. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(process.argv[2],'utf8');
const context=vm.createContext({});
vm.runInContext(source.slice(source.indexOf('const recentErrors=[];'),source.indexOf("window.addEventListener('error'")),context);
const technical=vm.runInContext("new TypeError(\"Cannot set properties of null (setting 'innerHTML')\")",context);
assert.doesNotMatch(context.humanError(technical),/innerHTML|null|TypeError/);
assert.match(context.humanError(technical),/Settings/);
assert.equal(vm.runInContext('recentErrors.length',context),1,'The same error should be retained once');
assert.match(vm.runInContext('recentErrors[0].message',context),/innerHTML/,'Technical details were lost');
assert.equal(context.humanError({message:'Choose a workspace first.',readable:true}),'Choose a workspace first.');
assert.match(context.humanError({name:'SyntaxError',message:'Unexpected token < in JSON'}),/couldn’t complete/);
assert.match(context.humanError({name:'TypeError',message:'Failed to fetch'}),/not responding/);
context.technicalError({message:'api_key=sk-fixture-secret authorization:Bearer private-token'});
assert.doesNotMatch(vm.runInContext('recentErrors.at(-1).message',context),/sk-fixture-secret|private-token/);
for(let i=0;i<30;i++)context.humanError({name:'TypeError',message:'fixture '+i});
assert.equal(vm.runInContext('recentErrors.length',context),12,'Diagnostics must stay bounded');
console.log('Readable UI errors passed: actionable messages, retained diagnostics, redaction and bounded storage.');
