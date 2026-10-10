# XR Universe Studio — صور إضافية (النسخة 2)

هالمرة بدنا **6 صور**، وكلها لنفس "الموديل": **مانيكان أزياء ثلاثي الأبعاد بجسم كامل**، أنيق ولامع، ومن دون إنسان حقيقي. منستخدمه حتى تصير تجربة اللبس الافتراضية مفهومة وواقعية: الملابس والإكسسوارات بتتبدل على المانيكان **جوّا شاشة المرآة وشاشة الموبايل**، بدل ما تطير قدّام الشاشة.

---

## قبل ما تبلّش (مهم)

1. **الاتساق أهم شي:** لازم يكون المانيكان نفسه بكل الصور، بنفس الوقفة ونفس الإطار. هيك بقدر أعمل انتقال سلس بين الإطلالات، متل ما بيصير بمرآة حقيقية.
   - **الطريقة الأفضل:** ولّد **A01** أول شي. بعدين استخدم ميزة **تعديل الصورة** (Edit) على A01 نفسها، لتطلع A02 وA03 منها.
   - كمان ولّد **A04** أول شي، واعمل **A05** بالتعديل عليها.
   - ميزة التعديل موجودة بـChatGPT وGPT-Image، وبـMidjourney اسمها Vary Region، وبأدوات تانية اسمها Inpaint.
2. **الخلفية:** شفافة (PNG). وإذا الأداة ما بتدعمها، خليها سوداء صافية.
3. **الإطار:**
   - **A01 لـA03:** جسم كامل من الراس للقدمين، واقف للأمام بنص الصورة، مع فراغ صغير فوق الراس وتحت القدمين. شاشة المرآة طويلة وضيقة، فلا تخلي الأيدين مفتوحة لبعيد.
   - **A04 وA05:** لقطة قريبة للوجه والكتفين، متل كاميرا سيلفي.
4. **المقاس:** 9:16 عمودي لكل الصور، وعلى الأقل 1152×2048.
5. **ممنوع:** نصوص، أو شعارات، أو علامات تجارية على الملابس، أو إنسان حقيقي.
6. **التسليم:** سمّيها بالأسماء المكتوبة جنبها، وابعتيها هون أو ارفعيها على `studio-ad/images/`.

> **ملاحظة:** كتبت المانيكان بقوام نسائي، لأنه الأشهر بعرض الأزياء. إذا بدك قوام رجالي أو حيادي، غيّري كلمة `female-form` بالبرومبتات لـ`male-form` أو `gender-neutral`. ونفس الشي إذا بدك تغيري الملابس.

### بصمة الأسلوب (نفس صور النسخة 1)
```
premium 3D render, soft studio lighting, glossy satin and iridescent glass materials,
color palette deep violet #5B3F8F, cyan #4FC3E0, magenta #E2367A, warm cream #F8EDE0,
subtle rim light, clean modern tech aesthetic, octane render, high detail, sharp focus
```

---

## المرآة (جسم كامل)

### A01 — المانيكان بلبس أساسي · `A01_body_base.png`
**المقاس:** 9:16 · **خلفية:** شفافة
> مانيكان لؤلؤي لامع، وجهه بملامح منحوتة ناعمة من غير شعر. لابس لبس أساسي بسيط بلون كريمي: بلوزة ضيقة وبنطلون. هاد "الموديل" الأساسي اللي منبني عليه الإطلالات.
```
a sleek stylized female-form fashion mannequin, full body from head to feet, standing straight facing the camera, perfectly centered, arms relaxed close to the body, smooth glossy pearl-white surface with subtle iridescent violet and cyan sheen, elegant softly sculpted face with gently closed eyes, no hair, bald smooth head, wearing a simple fitted warm-cream long-sleeve top and slim cream trousers with minimal white sneakers, small empty space above the head and below the feet, premium 3D render, soft studio lighting, glossy satin and iridescent glass materials, color palette deep violet #5B3F8F, cyan #4FC3E0, magenta #E2367A, warm cream #F8EDE0, subtle rim light, clean modern tech aesthetic, octane render, high detail, sharp focus, isolated on a transparent background
```

### A02 — إطلالة 1: ستريت ستايل · `A02_body_outfit1.png`
**المقاس:** 9:16 · **خلفية:** شفافة · **الطريقة:** تعديل على A01
> نفس المانيكان لابس جاكيت بومبر بنفسجي لامع، والطاقية والنظارة متل اللي بصورة M02. هيك بترتبط بقائمة الأغراض جوّا المرآة.
```
edit this image: keep the exact same mannequin, same pose, same framing, same lighting and background. Change the outfit to: a glossy iridescent violet satin bomber jacket over a cream t-shirt, slim black cargo trousers, chunky white-and-cyan sneakers, a glossy iridescent purple baseball cap, translucent pink-violet cat-eye sunglasses with gradient purple lenses, and glossy magenta lipstick. Clothes fit the body realistically with natural folds, correct scale and contact shadows. No logos. premium 3D render, same style
```

### A03 — إطلالة 2: سهرة · `A03_body_outfit2.png`
**المقاس:** 9:16 · **خلفية:** شفافة · **الطريقة:** تعديل على A01
> نفس المانيكان لابس فستان سهرة طويل من الساتان الفوشيا، مع حلق وشنطة صغيرة. منستعملها حتى نبيّن تبديل الإطلالة بلمسة.
```
edit this image: keep the exact same mannequin, same pose, same framing, same lighting and background. Change the outfit to: an elegant floor-length magenta-to-violet satin evening gown with a soft drape, delicate rose-gold drop earrings, and a small iridescent cream clutch bag held in one hand. The dress fits the body realistically with natural satin folds and highlights. No logos. premium 3D render, same style
```

### A06 — نفس المانيكان من الخلف (الحقيقي، واقف قدّام المرآة) · `A06_body_back.png`
**المقاس:** 9:16 · **خلفية:** شفافة · **الطريقة:** توليد جديد (التعديل ما بيقدر يلفّ المانيكان)
> هاد المانيكان "الحقيقي" اللي واقف قدّام المرآة، وظهره للكاميرا، ولابس **اللبس الأساسي نفسه** تبع A01. لازم يكون نفس اللون ونفس الملابس، حتى ينفهم إنه هو نفسه اللي ظاهر بالشاشة.
```
a sleek stylized female-form fashion mannequin seen from behind, full body from head to feet, rear view, standing straight, arms relaxed close to the body, smooth glossy pearl-white surface with subtle iridescent violet and cyan sheen, no hair, bald smooth head, wearing a simple fitted warm-cream long-sleeve top and slim cream trousers with minimal white sneakers, small empty space above the head and below the feet, premium 3D render, soft studio lighting, glossy satin and iridescent glass materials, color palette deep violet #5B3F8F, cyan #4FC3E0, magenta #E2367A, warm cream #F8EDE0, subtle rim light, clean modern tech aesthetic, octane render, high detail, sharp focus, isolated on a transparent background
```

---

## الفلاتر (لقطة سيلفي قريبة)

### A04 — وجه المانيكان قريب · `A04_face_bare.png`
**المقاس:** 9:16 · **خلفية:** شفافة
> نفس المانيكان بلقطة قريبة متل كاميرا السيلفي: الوجه والرقبة وبداية الكتفين، مع فراغ فوق الراس منحط فيه أذنين الفلتر.
```
close-up selfie-style portrait of the same sleek stylized female-form fashion mannequin, head neck and top of the shoulders, facing the camera straight on, centered, smooth glossy pearl-white surface with subtle iridescent violet and cyan sheen, elegant softly sculpted face with gently closed eyes, calm expression, no hair, bald smooth head, wearing the collar of a simple cream top, generous empty space above the head, premium 3D render, soft studio lighting, glossy satin and iridescent glass materials, color palette deep violet #5B3F8F, cyan #4FC3E0, magenta #E2367A, warm cream #F8EDE0, subtle rim light, clean modern tech aesthetic, octane render, high detail, sharp focus, isolated on a transparent background
```

### A05 — نفس الوجه مع فلتر أذنين أرنب · `A05_face_filter.png`
**المقاس:** 9:16 · **خلفية:** شفافة · **الطريقة:** تعديل على A04
> فلتر مرح متل فلاتر سناب شات: أذنين أرنب لؤلؤية، وتاج صغير، ونظارة قلوب، ونجوم وقلوب لامعة طايرة حوالين الراس.
```
edit this image: keep the exact same mannequin face, same pose, same framing, same lighting and background. Add a playful augmented-reality face filter: tall iridescent pearl bunny ears on a purple headband with small bows, a small rose-gold crown with heart gems on top of the head, heart-shaped rose-gold sunglasses with pink-purple gradient lenses worn on the face, and a few small glossy 3D stars and hearts floating around the head in cyan, magenta and cream. Everything fits the head with correct scale and soft glow. premium 3D render, same style
```

---

## وين بتروح كل صورة

| المشهد | قبل | بعد |
|---|---|---|
| **3 — مرآة الواقع المعزز** | الأغراض بتطير قدّام الشاشة | المانيكان الحقيقي (A06) واقف قدّام المرآة وظهره إلنا، ولابس اللبس الأساسي. جوّا الشاشة بيبيّن انعكاسه من القدّام (A01)، وبتمسح عليه شبكة تتبع الجسم. بتطلع قائمة إطلالات صغيرة جوّا واجهة المرآة، ولما تنختار وحدة بيتبدل لبسه **بالشاشة بس** بمسحة ضوئية ← A02 ← A03، والمانيكان الحقيقي بيضل بلبسه الأساسي. هاد هو سحر الـAR. بعدين بيدخل موبايل جنب المرآة عليه نفس التجربة، وبيطلع نص «بالمتجر أو من موبايلك». |
| **5 — الفلاتر** | الأذنين والتاج على شاشة فاضية | جوّا شاشة السيلفي بيبيّن الوجه (A04) مع نقاط تتبع الوجه، والفلتر بينطبق ← A05. |
| **1 — المنتجات (من غير صور جديدة)** | العطر بيطلع من الشاشة لبرا | جوّا شاشة الموبايل بيبيّن منظر الكاميرا للأرضية، وعليه مؤشر تموضع AR، وبعدين بيتحط العطر عليه. |
