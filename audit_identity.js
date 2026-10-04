const fs = require('fs'); const vm = require('vm');
const personData = JSON.parse(fs.readFileSync('app/src/main/assets/person_i18n.json','utf8'));
const code = fs.readFileSync('app/src/main/assets/js/quiz.js','utf8');
const langs = personData.languages;
let leaks=[];
for (const lang of langs) {
  const ctx = {ALL_DATA:{}, window:{PERSON_I18N:personData}, I18N:{}, console};
  vm.createContext(ctx);
  vm.runInContext(`let currentLang=${JSON.stringify(lang)};\n${code}`, ctx);
  for (const [key, obj] of Object.entries(personData.people)) {
    const p={name_en:key,name:key};
    const bundle=obj.languages?.[lang]||{};
    const fields=['bio','hint','achievements','key_facts','historical_significance'];
    const ids=ctx.cardIdentityVariants(p);
    for (const field of fields) {
      const raw=bundle[field];
      const values=Array.isArray(raw)?raw:(raw?[raw]:[]);
      for (const item of values) {
        const safe=ctx.sanitizeCardText(item,p);
        for (const id of ids) {
          if (id && ctx.identityRegex(id).test(String(safe))) leaks.push({key,lang,field,id,safe});
        }
      }
    }
  }
}
console.log(JSON.stringify({people:Object.keys(personData.people).length,languages:langs.length,leaks:leaks.length,examples:leaks.slice(0,30)},null,2));
process.exitCode=leaks.length?1:0;
