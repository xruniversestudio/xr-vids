# XR Universe Studio — صور إضافية (النسخة 2)

هالمرة بدنا **3 صور بس**، وكلها لنفس "الموديل": **رأس مانيكان ثلاثي الأبعاد**، أنيق ولامع، ومن دون إنسان حقيقي. منستخدمه حتى تصير التجربة الافتراضية مفهومة وواقعية: الأغراض بتنلبس على الرأس **جوّا شاشة المرآة وشاشة الموبايل**، بدل ما تطير قدّام الشاشة.

---

## قبل ما تبلّش (مهم)

1. **الاتساق أهم شي:** لازم يكون الرأس نفسه بالصور الثلاث، بنفس الوضعية ونفس الإطار. هيك بقدر أعمل انتقال سلس من "بدون أغراض" لـ"مع أغراض".
   - **الطريقة الأفضل:** ولّد **A01** أول شي. بعدين استخدم ميزة **تعديل الصورة** (Edit) على A01 نفسها، لتطلع A02 وA03 منها.
   - هالميزة موجودة بـChatGPT وGPT-Image، وبـMidjourney اسمها Vary Region، وبأدوات تانية اسمها Inpaint.
   - إذا ولّدتها من الصفر بيتغير الرأس والزاوية، وما بيزبط الانتقال.
2. **الخلفية:** شفافة (PNG). وإذا الأداة ما بتدعمها، خليها سوداء صافية.
3. **المقاس:** 3:4 عمودي، وعلى الأقل 1536×2048.
4. **الإطار:** الرأس والرقبة وبداية الكتفين، والوجه للأمام تماماً وبنص الصورة. اتركي فراغ صغير فوق الرأس، حتى يكون في محل لأذنين الأرنب والتاج بـA03.
5. **ممنوع:** نصوص، أو شعارات، أو علامات تجارية، أو إنسان حقيقي.
6. **التسليم:** سمّيها بالأسماء المكتوبة جنبها، وابعتيها هون أو ارفعيها على `studio-ad/images/`.

### بصمة الأسلوب (نفس صور النسخة 1)
```
premium 3D render, soft studio lighting, glossy satin and iridescent glass materials,
color palette deep violet #5B3F8F, cyan #4FC3E0, magenta #E2367A, warm cream #F8EDE0,
subtle rim light, clean modern tech aesthetic, octane render, high detail, sharp focus
```

---

### A01 — رأس المانيكان بدون أغراض · `A01_bust_bare.png`
**المقاس:** 3:4 · **خلفية:** شفافة
> رأس مانيكان لؤلؤي لامع، ملامحه منحوتة ناعمة، وعيونه مسكّرة بهدوء. من غير شعر، والوجه للأمام. هاد "الموديل" الأساسي اللي منبني عليه الصورتين التانيتين.
```
a sleek stylized mannequin head and shoulders bust, front view, perfectly centered and symmetrical, facing the camera straight on, smooth glossy pearl-white surface with subtle iridescent violet and cyan sheen, elegant softly sculpted facial features, gently closed eyes, neutral calm expression, no hair, bald smooth head, slim neck, top of the shoulders visible, empty space above the head, premium 3D render, soft studio lighting, glossy satin and iridescent glass materials, color palette deep violet #5B3F8F, cyan #4FC3E0, magenta #E2367A, warm cream #F8EDE0, subtle rim light, clean modern tech aesthetic, octane render, high detail, sharp focus, isolated on a transparent background
```

### A02 — نفس الرأس لابس طاقية ونظارة وأحمر شفاه · `A02_bust_tryon.png`
**المقاس:** 3:4 · **خلفية:** شفافة · **الطريقة:** تعديل على A01
> الأغراض نفسها اللي بصورة M02: طاقية بنفسجي لامعة، ونظارة شمسية شفافة بإطار زهري وعدسات متدرجة، وأحمر شفاه فوشيا على الشفاه. منستخدمها جوّا شاشة المرآة وجوّا شاشة الموبايل.
```
edit this image: keep the exact same mannequin bust, same pose, same framing, same lighting and background. Add: a glossy iridescent purple baseball cap worn naturally on the head, translucent pink-violet cat-eye sunglasses with gradient purple lenses and small gold details worn on the face, and glossy magenta lipstick on the lips. The items must fit the head realistically with correct scale, contact shadows and reflections. premium 3D render, same style
```
**إذا بدك تولّديها من الصفر** (ولو إنه مش مفضّل)، استعملي برومبت A01 كامل، وزيدي عليه بعد `no hair,` هالجملة:
`wearing a glossy iridescent purple baseball cap, translucent pink-violet cat-eye sunglasses with gradient purple lenses, glossy magenta lipstick,`

### A03 — نفس الرأس مع فلتر أذنين أرنب · `A03_bust_filter.png`
**المقاس:** 3:4 · **خلفية:** شفافة · **الطريقة:** تعديل على A01
> فلتر مرح متل فلاتر سناب شات: أذنين أرنب لؤلؤية، وتاج ذهبي صغير، ونظارة على شكل قلوب، ونجوم وقلوب لامعة صغيرة طايرة حوالين الرأس.
```
edit this image: keep the exact same mannequin bust, same pose, same framing, same lighting and background. Add a playful augmented-reality face filter: tall iridescent pearl bunny ears on a purple headband with small bows, a small rose-gold crown with heart gems on top of the head, heart-shaped rose-gold sunglasses with pink-purple gradient lenses worn on the face, and a few small glossy 3D stars and hearts floating around the head in cyan, magenta and cream. Everything fits the head with correct scale and soft glow. premium 3D render, same style
```

---

## وين بتروح كل صورة

| المشهد | قبل | بعد |
|---|---|---|
| **3 — مرآة الواقع المعزز** | الأغراض بتطير قدّام الشاشة | جوّا شاشة المرآة بيبيّن A01، وشبكة تتبع الوجه بتمسح عليه. بتطلع قائمة أغراض صغيرة جوّا واجهة المرآة (من M02)، ولما ينختار الغرض بيصير A02 كأنه انلبس فعلاً. بعدين بيدخل موبايل جنب المرآة عليه نفس التجربة، وبيطلع نص «بالمتجر أو من موبايلك». |
| **5 — الفلاتر** | الأذنين والتاج على شاشة فاضية | جوّا شاشة السيلفي بيبيّن A01 مع شبكة تتبع، والفلتر بينطبق ← A03. |
| **1 — المنتجات (من غير صور جديدة)** | العطر بيطلع من الشاشة لبرا | جوّا شاشة الموبايل بيبيّن منظر الكاميرا للأرضية، وعليه مؤشر تموضع AR، وبعدين بيتحط العطر عليه. |
