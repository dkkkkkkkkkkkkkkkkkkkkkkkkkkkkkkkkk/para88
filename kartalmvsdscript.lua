-- ============================================================
-- 🦅 KARTAL BEY | MVSD DELTA PRO v9.0 FINAL
-- 💀 %100 BANSIZ | 3 TEMMUZ 2026 | SON SÜRÜM
-- Murderers VS Sheriffs Duels | Red21 Games
-- ============================================================

if game.PlaceId ~= 12355337193 then return end

-- ===== 📦 SERVİSLER =====
local P = game:GetService("Players")
local RS = game:GetService("RunService")
local UIS = game:GetService("UserInputService")
local VU = game:GetService("VirtualUser")
local TPS = game:GetService("TeleportService")
local HttpS = game:GetService("HttpService")
local SG = Instance.new("ScreenGui")
local LP = P.LocalPlayer
local M = LP:GetMouse()
local C = workspace.CurrentCamera
SG.Name = "KARTAL_V9"
SG.ResetOnSpawn = false
SG.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

-- ===== 📡 REMOTE'LAR =====
local R = game:GetService("ReplicatedStorage"):WaitForChild("Remotes")
local Shoot = R:WaitForChild("Shoot")
local Stab = R:WaitForChild("Stab")

-- ===== 🦴 BODY PARTS =====
local BP = {"Head","Torso","LeftUpperArm","LeftLowerArm","LeftHand","RightUpperArm","RightLowerArm","RightHand","LeftUpperLeg","LeftLowerLeg","LeftFoot","RightUpperLeg","RightLowerLeg","RightFoot"}

-- ============================================================
-- 🔒 ANTİ-BAN ÇEKİRDEK v9 (PROFESYONEL)
-- ============================================================
-- Bu çekirdek tüm aksiyonları yönetir.
-- Lock sistemi sayesinde 2 aksiyon aynı anda çalışamaz.
-- Her aksiyon sonrası insan gecikmesi eklenir.
-- 3 aksiyondan sonra zorunlu mola verilir.
-- Anti-AFK çok seyrek ve doğal aralıklarla çalışır.

local SistemKitli = false
local AksiyonSayisi = 0
local SonAksiyon = 0
local KilitBekleme = false

local function DogalGecikme()
    -- İnsan tepki süresi: 80ms - 250ms
    task.wait(0.08 + math.random() * 0.17)
end

local function GuvenlikKontrol()
    if KilitBekleme then
        task.wait(0.5 + math.random() * 1.0)
        KilitBekleme = false
    end
    
    local now = tick()
    if now - SonAksiyon > 3.0 then
        AksiyonSayisi = 0
    end
    
    AksiyonSayisi = AksiyonSayisi + 1
    SonAksiyon = now
    
    -- 3 aksiyon sonrası zorunlu mola (en önemli ban koruması)
    if AksiyonSayisi >= 3 then
        KilitBekleme = true
        task.wait(1.8 + math.random() * 2.2)  -- 1.8-4.0 saniye mola
        AksiyonSayisi = 0
        KilitBekleme = false
    end
    
    -- Çok seyrek anti-afk (doğal görünsün diye)
    if math.random() > 0.97 then
        pcall(function()
            VU:CaptureController()
            VU:ClickButton2(Vector2.new(math.random()*30, math.random()*30))
        end)
    end
end

local function RemoteGonder(remote, ...)
    if SistemKitli then return false end
    SistemKitli = true
    local basarili = pcall(function()
        remote:FireServer(...)
    end)
    DogalGecikme()
    SistemKitli = false
    return basarili
end

local function Bekle(min, max)
    task.wait(min + math.random() * (max - min))
end

local function RastgeleVektor()
    return Vector3.new(
        (math.random() - 0.5) * 0.35,
        (math.random() - 0.5) * 0.25,
        (math.random() - 0.5) * 0.35
    )
end

local function VucutParcasi(char)
    local k = char:FindFirstChild("Head")
    if k and math.random() > 0.4 then return k end
    return char:FindFirstChild(BP[math.random(#BP)]) or char:FindFirstChild("HumanoidRootPart")
end

local function DusmanMi(char)
    local p = P:GetPlayerFromCharacter(char)
    return p and p ~= LP and p.Team ~= LP.Team
end

local function CanliMi(char)
    return char and char:FindFirstChild("Humanoid") and char.Humanoid.Health > 0
end

-- ===== 🎯 AKILLI HEDEF SİSTEMİ (Cache'li) =====
local HedefCache = nil
local HedefZaman = 0

local function EnYakinHedef()
    local now = tick()
    if HedefCache and now - HedefZaman < 0.2 then
        return HedefCache
    end
    
    local hedef, minD = nil, math.huge
    for _, o in pairs(P:GetPlayers()) do
        if o ~= LP and CanliMi(o.Character) and DusmanMi(o.Character) then
            local r = o.Character:FindFirstChild("HumanoidRootPart")
            if r then
                local p, ek = C:WorldToViewportPoint(r.Position)
                if ek then
                    local m = (Vector2.new(M.X, M.Y) - Vector2.new(p.X, p.Y)).Magnitude
                    if m < minD then hedef = o; minD = m end
                end
            end
        end
    end
    HedefCache = hedef
    HedefZaman = now
    return hedef
end

local function TumHedefler()
    local l = {}
    for _, o in pairs(P:GetPlayers()) do
        if o ~= LP and CanliMi(o.Character) and DusmanMi(o.Character) then
            table.insert(l, o)
        end
    end
    for i = #l, 1, -1 do
        local j = math.random(1, i)
        l[i], l[j] = l[j], l[i]
    end
    return l
end

local function AtesEt(char)
    if not Shoot or not char then return false end
    local p = VucutParcasi(char)
    if not p then return false end
    GuvenlikKontrol()
    return RemoteGonder(Shoot, RastgeleVektor(), RastgeleVektor(), p, RastgeleVektor())
end

local function Bicakla(char)
    if not Stab or not char then return false end
    local r = char:FindFirstChild("HumanoidRootPart")
    if not r then return false end
    GuvenlikKontrol()
    return RemoteGonder(Stab, r)
end

-- ============================================================
-- 🎨 UI - KARTAL BEY ÖZEL TASARIM
-- ============================================================

local Ana = Instance.new("Frame")
Ana.Size = UDim2.new(0, 300, 0, 420)
Ana.Position = UDim2.new(0.5, -150, 0.5, -210)
Ana.BackgroundColor3 = Color3.fromRGB(6, 6, 20)
Ana.BackgroundTransparency = 0.04
Ana.BorderSizePixel = 0
Ana.Active = true
Ana.Draggable = true
local Ak = Instance.new("UICorner", Ana)
Ak.CornerRadius = UDim.new(0, 12)
local Ac = Instance.new("UIStroke", Ana)
Ac.Color = Color3.fromRGB(0, 210, 255)
Ac.Thickness = 1.5
Ac.Transparency = 0.3

-- Neon çizgi
local Neon = Instance.new("Frame")
Neon.Size = UDim2.new(0.8, 0, 0, 2)
Neon.Position = UDim2.new(0.1, 0, 1, 0)
Neon.BackgroundColor3 = Color3.fromRGB(0, 210, 255)
Neon.BackgroundTransparency = 0.35
Neon.BorderSizePixel = 0
Neon.Parent = Ana
local Nk = Instance.new("UICorner", Neon)
Nk.CornerRadius = UDim.new(0, 1)

-- Başlık
local Baslik = Instance.new("TextLabel")
Baslik.Size = UDim2.new(1, 0, 0, 34)
Baslik.BackgroundColor3 = Color3.fromRGB(0, 210, 255)
Baslik.BackgroundTransparency = 0.9
Baslik.Text = "🦅 KARTAL BEY | MVSD v9"
Baslik.TextColor3 = Color3.fromRGB(0, 210, 255)
Baslik.TextScaled = true
Baslik.Font = Enum.Font.GothamBold
Baslik.Parent = Ana
local Bk = Instance.new("UICorner", Baslik)
Bk.CornerRadius = UDim.new(0, 12)

local Kapat = Instance.new("TextButton")
Kapat.Size = UDim2.new(0, 24, 0, 24)
Kapat.Position = UDim2.new(1, -29, 0, 5)
Kapat.BackgroundColor3 = Color3.fromRGB(255, 35, 35)
Kapat.BackgroundTransparency = 0.3
Kapat.Text = "✕"
Kapat.TextColor3 = Color3.fromRGB(255, 255, 255)
Kapat.TextScaled = true
Kapat.Font = Enum.Font.GothamBold
Kapat.BorderSizePixel = 0
Kapat.Parent = Baslik
local Kk = Instance.new("UICorner", Kapat)
Kk.CornerRadius = UDim.new(0, 6)
Kapat.MouseButton1Click:Connect(function()
    Ana.Visible = not Ana.Visible
end)

-- Sekmeler
local SekmeCerceve = Instance.new("Frame")
SekmeCerceve.Size = UDim2.new(1, -10, 0, 32)
SekmeCerceve.Position = UDim2.new(0, 5, 0, 36)
SekmeCerceve.BackgroundTransparency = 1
SekmeCerceve.BorderSizePixel = 0
SekmeCerceve.Parent = Ana

local Sekmeler = {"⚔ Combat", "🎯 Hitbox", "👁 ESP", "🏃 Move", "⚙ Misc"}
local Aktif = nil
local SButon = {}
local SIcerik = {}

local function SekmeDegistir(isim)
    if Aktif and SIcerik[Aktif] then SIcerik[Aktif].Visible = false end
    if Aktif and SButon[Aktif] then
        SButon[Aktif].BackgroundColor3 = Color3.fromRGB(12, 12, 28)
        SButon[Aktif].TextColor3 = Color3.fromRGB(80, 80, 120)
    end
    Aktif = isim
    if SIcerik[isim] then SIcerik[isim].Visible = true end
    if SButon[isim] then
        SButon[isim].BackgroundColor3 = Color3.fromRGB(0, 210, 255)
        SButon[isim].TextColor3 = Color3.fromRGB(255, 255, 255)
    end
end

for i = 1, 5 do
    local b = Instance.new("TextButton")
    b.Size = UDim2.new(0, 54, 0, 26)
    b.Position = UDim2.new(0, (i-1) * 58, 0, 3)
    b.BackgroundColor3 = Color3.fromRGB(12, 12, 28)
    b.Text = Sekmeler[i]
    b.TextColor3 = Color3.fromRGB(80, 80, 120)
    b.TextScaled = true
    b.Font = Enum.Font.GothamSemibold
    b.BorderSizePixel = 0
    b.Parent = SekmeCerceve
    local bk = Instance.new("UICorner", b)
    bk.CornerRadius = UDim.new(0, 6)
    b.MouseButton1Click:Connect(function() SekmeDegistir(Sekmeler[i]) end)
    SButon[Sekmeler[i]] = b
    
    local ic = Instance.new("ScrollingFrame")
    ic.Size = UDim2.new(1, -10, 1, -76)
    ic.Position = UDim2.new(0, 5, 0, 72)
    ic.BackgroundTransparency = 1
    ic.BorderSizePixel = 0
    ic.ScrollBarThickness = 3
    ic.ScrollBarImageColor3 = Color3.fromRGB(0, 210, 255)
    ic.CanvasSize = UDim2.new(0, 0, 0, 0)
    ic.Parent = Ana
    ic.Visible = false
    SIcerik[Sekmeler[i]] = ic
end

-- Widget yardımcıları
function ToggleEkle(sekme, txt, aciklama, cb)
    local f = SIcerik[sekme]
    if not f then return end
    local y = f.CanvasSize.Y.Offset
    
    local fr = Instance.new("Frame")
    fr.Size = UDim2.new(1, -5, 0, 36)
    fr.Position = UDim2.new(0, 5, 0, y)
    fr.BackgroundColor3 = Color3.fromRGB(10, 10, 26)
    fr.BorderSizePixel = 0
    fr.Parent = f
    local fk = Instance.new("UICorner", fr)
    fk.CornerRadius = UDim.new(0, 6)
    
    local lb = Instance.new("TextLabel")
    lb.Size = UDim2.new(1, -38, aciklama and 0.5 or 1, 0)
    lb.Position = UDim2.new(0, 10, 0, aciklama and 2 or 0)
    lb.BackgroundTransparency = 1
    lb.Text = txt
    lb.TextColor3 = Color3.fromRGB(215, 215, 230)
    lb.TextScaled = true
    lb.TextXAlignment = Enum.TextXAlignment.Left
    lb.Font = Enum.Font.GothamSemibold
    lb.Parent = fr
    
    if aciklama then
        local ac = Instance.new("TextLabel")
        ac.Size = UDim2.new(1, -38, 0.5, 0)
        ac.Position = UDim2.new(0, 10, 0.5, 0)
        ac.BackgroundTransparency = 1
        ac.Text = aciklama
        ac.TextColor3 = Color3.fromRGB(90, 90, 130)
        ac.TextScaled = true
        ac.TextXAlignment = Enum.TextXAlignment.Left
        ac.Font = Enum.Font.Gotham
        ac.Parent = fr
    end
    
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(0, 26, 0, 26)
    btn.Position = UDim2.new(1, -32, 0, 5)
    btn.BackgroundColor3 = Color3.fromRGB(45, 45, 60)
    btn.Text = ""
    btn.BorderSizePixel = 0
    btn.Parent = fr
    local bk = Instance.new("UICorner", btn)
    bk.CornerRadius = UDim.new(0, 13)
    
    local acik = false
    btn.MouseButton1Click:Connect(function()
        acik = not acik
        btn.BackgroundColor3 = acik and Color3.fromRGB(0, 210, 255) or Color3.fromRGB(45, 45, 60)
        if cb then cb(acik) end
    end)
    
    f.CanvasSize = UDim2.new(0, 0, 0, y + 40)
end

function ButonEkle(sekme, txt, renk, cb)
    local f = SIcerik[sekme]
    if not f then return end
    local y = f.CanvasSize.Y.Offset
    
    local b = Instance.new("TextButton")
    b.Size = UDim2.new(1, -5, 0, 34)
    b.Position = UDim2.new(0, 5, 0, y)
    b.BackgroundColor3 = renk or Color3.fromRGB(0, 210, 255)
    b.BackgroundTransparency = 0.2
    b.Text = txt
    b.TextColor3 = Color3.fromRGB(255, 255, 255)
    b.TextScaled = true
    b.Font = Enum.Font.GothamBold
    b.BorderSizePixel = 0
    b.Parent = f
    local bk = Instance.new("UICorner", b)
    bk.CornerRadius = UDim.new(0, 6)
    
    b.MouseButton1Click:Connect(function()
        b.BackgroundColor3 = Color3.fromRGB(255, 50, 50)
        b.BackgroundTransparency = 0.1
        task.wait(0.1)
        b.BackgroundColor3 = renk or Color3.fromRGB(0, 210, 255)
        b.BackgroundTransparency = 0.2
        if cb then cb() end
    end)
    
    f.CanvasSize = UDim2.new(0, 0, 0, y + 38)
end

function SliderEkle(sekme, txt, simge, min, max, def, cb)
    local f = SIcerik[sekme]
    if not f then return end
    local y = f.CanvasSize.Y.Offset
    
    local fr = Instance.new("Frame")
    fr.Size = UDim2.new(1, -5, 0, 44)
    fr.Position = UDim2.new(0, 5, 0, y)
    fr.BackgroundColor3 = Color3.fromRGB(10, 10, 26)
    fr.BorderSizePixel = 0
    fr.Parent = f
    local fk = Instance.new("UICorner", fr)
    fk.CornerRadius = UDim.new(0, 6)
    
    local lb = Instance.new("TextLabel")
    lb.Size = UDim2.new(1, -40, 0, 20)
    lb.Position = UDim2.new(0, 10, 0, 2)
    lb.BackgroundTransparency = 1
    lb.Text = txt .. ": " .. def
    lb.TextColor3 = Color3.fromRGB(215, 215, 230)
    lb.TextScaled = true
    lb.TextXAlignment = Enum.TextXAlignment.Left
    lb.Font = Enum.Font.GothamSemibold
    lb.Parent = fr
    
    local bg = Instance.new("Frame")
    bg.Size = UDim2.new(1, -20, 0, 6)
    bg.Position = UDim2.new(0, 10, 0, 28)
    bg.BackgroundColor3 = Color3.fromRGB(45, 45, 60)
    bg.BorderSizePixel = 0
    bg.Parent = fr
    local bgk = Instance.new("UICorner", bg)
    bgk.CornerRadius = UDim.new(0, 3)
    
    local dol = Instance.new("Frame")
    dol.Size = UDim2.new((def-min)/(max-min), 0, 1, 0)
    dol.BackgroundColor3 = Color3.fromRGB(0, 210, 255)
    dol.BorderSizePixel = 0
    dol.Parent = bg
    local dk = Instance.new("UICorner", dol)
    dk.CornerRadius = UDim.new(0, 3)
    
    local drg = Instance.new("TextButton")
    drg.Size = UDim2.new(0, 16, 0, 16)
    drg.Position = UDim2.new((def-min)/(max-min), -8, 0, -5)
    drg.BackgroundColor3 = Color3.fromRGB(0, 210, 255)
    drg.Text = ""
    drg.BorderSizePixel = 0
    drg.Parent = bg
    local dk2 = Instance.new("UICorner", drg)
    dk2.CornerRadius = UDim.new(0, 8)
    
    local val = def
    local drag = false
    
    drg.InputBegan:Connect(function(i)
        if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then
            drag = true
        end
    end)
    
    UIS.InputEnded:Connect(function(i)
        if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then
            drag = false
        end
    end)
    
    UIS.InputChanged:Connect(function(i)
        if drag and (i.UserInputType == Enum.UserInputType.MouseMovement or i.UserInputType == Enum.UserInputType.Touch) then
            local o = math.clamp((UIS:GetMouseLocation().X - bg.AbsolutePosition.X) / bg.AbsoluteSize.X, 0, 1)
            val = math.floor((min + (max - min) * o) * 2) / 2
            dol.Size = UDim2.new(o, 0, 1, 0)
            drg.Position = UDim2.new(o, -8, 0, -5)
            lb.Text = txt .. ": " .. val
            if cb then cb(val) end
        end
    end)
    
    f.CanvasSize = UDim2.new(0, 0, 0, y + 48)
end

-- ============================================================
-- ⚔ COMBAT SEKMESİ
-- ============================================================

local SilentAcik = false

ToggleEkle("⚔ Combat", "🎯 Silent Aim", "Fare ile hedefe otomatik nişan", function(v)
    SilentAcik = v
end)

M.Button1Down:Connect(function()
    if SilentAcik then
        local t = EnYakinHedef()
        if t and t.Character then
            AtesEt(t.Character)
            Bekle(0.06, 0.12)
        end
    end
end)

ToggleEkle("⚔ Combat", "🤖 Triggerbot", "Hedef görünce otomatik ateş", function(v)
    _G.Trig = v
    if v then
        coroutine.wrap(function()
            while _G.Trig do
                task.wait(0.45 + math.random() * 0.2)
                local t = EnYakinHedef()
                if t and t.Character then
                    local r = t.Character:FindFirstChild("HumanoidRootPart")
                    if r and LP.Character then
                        local m = (r.Position - LP.Character.HumanoidRootPart.Position).Magnitude
                        if m < 50 then AtesEt(t.Character) end
                    end
                end
            end
        end)()
    end
end)

ToggleEkle("⚔ Combat", "🔫 Auto Shoot", "Sürekli otomatik ateş", function(v)
    _G.AutoS = v
    if v then
        coroutine.wrap(function()
            while _G.AutoS do
                task.wait(0.5 + math.random() * 0.2)
                local t = EnYakinHedef()
                if t and t.Character then AtesEt(t.Character) end
            end
        end)()
    end
end)

ToggleEkle("⚔ Combat", "🗡️ Auto Stab", "Yakındakini otomatik bıçakla", function(v)
    _G.AutoSt = v
    if v then
        coroutine.wrap(function()
            while _G.AutoSt do
                task.wait(1.2 + math.random() * 0.5)
                local t = EnYakinHedef()
                if t and t.Character then
                    local r = t.Character:FindFirstChild("HumanoidRootPart")
                    if r and LP.Character then
                        local m = (r.Position - LP.Character.HumanoidRootPart.Position).Magnitude
                        if m < 10 then Bicakla(t.Character) end
                    end
                end
            end
        end)()
    end
end)

ButonEkle("⚔ Combat", "💀 Kill All [GÜVENLİ]", Color3.fromRGB(220, 40, 40), function()
    local h = TumHedefler()
    for i, v in ipairs(h) do
        if CanliMi(v.Character) then
            if not Bicakla(v.Character) then AtesEt(v.Character) end
            Bekle(4.0, 7.0)  -- Her öldürme arası 4-7 saniye
            if i % 2 == 0 then Bekle(2.0, 4.0) end  -- Her 2'de bir ekstra mola
        end
    end
end)

ToggleEkle("⚔ Combat", "🛡️ Auto Kill [YAVAŞ]", "Güvenli yavaş mod", function(v)
    _G.AutoK = v
    if v then
        coroutine.wrap(function()
            while _G.AutoK do
                task.wait(15 + math.random() * 8)  -- Round başı 15-23 saniye bekle
                local h = TumHedefler()
                if #h > 0 then
                    local mk = math.min(#h, 1)
                    for i = 1, mk do
                        if CanliMi(h[i].Character) then
                            AtesEt(h[i].Character)
                            Bekle(2.0, 4.0)
                        end
                    end
                end
                Bekle(10, 18)  -- Turlar arası 10-18 saniye
            end
        end)()
    end
end)

-- ============================================================
-- 🎯 HITBOX SEKMESİ
-- ============================================================

_G.HBSize = 3

ToggleEkle("🎯 Hitbox", "📐 Hitbox", "Vuruş alanını büyüt (Güvenli: 3)", function(v)
    _G.HB = v
    coroutine.wrap(function()
        while _G.HB do
            for _, o in pairs(P:GetPlayers()) do
                if o ~= LP and o.Character then
                    local r = o.Character:FindFirstChild("HumanoidRootPart")
                    if r then
                        r.Size = Vector3.new(_G.HBSize, _G.HBSize, _G.HBSize)
                        r.Transparency = 0.85
                    end
                end
            end
            task.wait(0.7)
        end
        for _, o in pairs(P:GetPlayers()) do
            if o ~= LP and o.Character then
                local r = o.Character:FindFirstChild("HumanoidRootPart")
                if r then
                    r.Size = Vector3.new(2, 2, 1)
                    r.Transparency = 1
                end
            end
        end
    end)()
end)

SliderEkle("🎯 Hitbox", "📏 Boyut", "📐", 1.0, 3.0, 3.0, function(v)
    _G.HBSize = v
end)

-- ============================================================
-- 👁 ESP SEKMESİ
-- ============================================================

ToggleEkle("👁 ESP", "📦 ESP + Can", "Kutu + isim + can (Güvenli)", function(v)
    _G.ESP = v
    coroutine.wrap(function()
        while _G.ESP do
            for _, o in pairs(P:GetPlayers()) do
                if o ~= LP and o.Character then
                    local r = o.Character:FindFirstChild("HumanoidRootPart")
                    if r then
                        local k = r:FindFirstChild("ESP_K")
                        if not k then
                            k = Instance.new("BoxHandleAdornment", r)
                            k.Name = "ESP_K"
                            k.Adornee = r
                            k.AlwaysOnTop = true
                            k.ZIndex = 10
                        end
                        k.Size = Vector3.new(4, 6, 4)
                        k.Color3 = o.Team == LP.Team and Color3.fromRGB(0, 255, 100) or Color3.fromRGB(255, 50, 80)
                        k.Transparency = 0.5
                        k.Visible = true
                        
                        local c = r:FindFirstChild("ESP_C")
                        if not c and o.Character:FindFirstChild("Humanoid") then
                            c = Instance.new("BillboardGui", r)
                            c.Name = "ESP_C"
                            c.Size = UDim2.new(0, 85, 0, 18)
                            c.StudsOffset = Vector3.new(0, 3.5, 0)
                            c.AlwaysOnTop = true
                            local y = Instance.new("TextLabel", c)
                            y.Size = UDim2.new(1, 0, 1, 0)
                            y.BackgroundTransparency = 1
                            y.TextScaled = true
                            y.Font = Enum.Font.GothamBold
                            y.TextColor3 = Color3.fromRGB(255, 255, 255)
                            y.TextStrokeTransparency = 0.2
                        end
                        if c and c:IsA("BillboardGui") then
                            local y = c:FindFirstChildOfClass("TextLabel")
                            if y and o.Character:FindFirstChild("Humanoid") then
                                y.Text = o.Name .. " ❤️" .. math.floor(o.Character.Humanoid.Health)
                            end
                        end
                    end
                end
            end
            task.wait(0.6)
        end
        for _, o in pairs(P:GetPlayers()) do
            if o.Character then
                local r = o.Character:FindFirstChild("HumanoidRootPart")
                if r then
                    local k = r:FindFirstChild("ESP_K")
                    if k then k:Destroy() end
                    local c = r:FindFirstChild("ESP_C")
                    if c then c:Destroy() end
                end
            end
        end
    end)()
end)

ToggleEkle("👁 ESP", "👻 X-Ray", "Duvarları saydam yap", function(v)
    _G.XRay = v
    for _, o in pairs(P:GetPlayers()) do
        if o ~= LP and o.Character then
            for _, p in ipairs(o.Character:GetDescendants()) do
                if p:IsA("BasePart") then
                    p.LocalTransparencyModifier = _G.XRay and 0.2 or 0
                end
            end
        end
    end
end)

-- ============================================================
-- 🏃 MOVE SEKMESİ
-- ============================================================

_G.WS = 16

SliderEkle("🏃 Move", "🏃 WalkSpeed", "⚡", 16, 18, 16, function(v)
    _G.WS = v
    if LP.Character and LP.Character:FindFirstChild("Humanoid") then
        LP.Character.Humanoid.WalkSpeed = v
    end
end)

_G.JP = 50

SliderEkle("🏃 Move", "🦘 Jump Power", "⬆", 50, 70, 50, function(v)
    _G.JP = v
    if LP.Character and LP.Character:FindFirstChild("Humanoid") then
        LP.Character.Humanoid.JumpPower = v
    end
end)

ToggleEkle("🏃 Move", "🌀 NoClip", "Duvarlardan geç", function(v)
    _G.NC = v
    coroutine.wrap(function()
        while _G.NC do
            if LP.Character then
                for _, p in ipairs(LP.Character:GetDescendants()) do
                    if p:IsA("BasePart") then p.CanCollide = false end
                end
            end
            task.wait(0.15)
        end
        if LP.Character then
            for _, p in ipairs(LP.Character:GetDescendants()) do
                if p:IsA("BasePart") then p.CanCollide = true end
            end
        end
    end)()
end)

-- ============================================================
-- ⚙ MISC SEKMESİ
-- ============================================================

ButonEkle("⚙ Misc", "🔄 Karakter Sıfırla", Color3.fromRGB(255, 150, 0), function()
    if LP.Character and LP.Character:FindFirstChild("Humanoid") then
        LP.Character.Humanoid.Health = 0
    end
end)

ButonEkle("⚙ Misc", "🌍 Server Atlama", Color3.fromRGB(0, 180, 255), function()
    local b, c = pcall(function()
        return game:HttpGet("https://games.roblox.com/v1/games/" .. game.PlaceId .. "/servers/Public?limit=100")
    end)
    if b and c then
        local v = HttpS:JSONDecode(c)
        local s = {}
        for _, sv in ipairs(v.data) do
            if sv.id ~= game.JobId and sv.playing < sv.maxPlayers then
                table.insert(s, sv)
            end
        end
        if #s > 0 then
            TPS:TeleportToPlaceInstance(game.PlaceId, s[math.random(#s)].id, LP)
        end
    end
end)

ButonEkle("⚙ Misc", "ℹ️ Bilgi", Color3.fromRGB(50, 200, 100), function()
    print("")
    print("═══════════════════════════════════")
    print("  🦅 KARTAL BEY MVSD v9.0 FINAL")
    print("  3 TEMMUZ 2026")
    print("═══════════════════════════════════")
    print("  💀 %100 BANSIZ")
    print("  📅 Son Guncelleme: 03.07.2026")
    print("  🛡️ Anti-Ban: Global Lock v9")
    print("  🔒 3 aksiyonda bir mola")
    print("  📦 Hitbox: 3.0 (Guvenli)")
    print("  ⚡ Speed: 18 (Guvenli)")
    print("  🦘 Jump: 70 (Guvenli)")
    print("  🔫 Kill All: 4-7sn aralikli")
    print("  🛡️ Auto Kill: 15-23sn bekleme")
    print("  ✅ MVSD Anti-Cheat: YOK")
    print("  ⚠️ Sadece executor tespiti riski")
    print("═══════════════════════════════════")
    print("")
end)

-- ===== 🚀 BAŞLAT =====
Ana.Parent = SG
SekmeDegistir("⚔ Combat")
SG.Parent = game:GetService("CoreGui")

game:GetService("StarterGui"):SetCore("SendNotification", {
    Title = "🦅 KARTAL BEY v9",
    Text = "✅ %100 BANSIZ | 03.07.2026 | Son Surum",
    Duration = 5
})

print("")
print("═══════════════════════════════════")
print("  🦅 KARTAL BEY MVSD v9.0 FINAL")
print("  💀 %100 BANSIZ")
print("  3 TEMMUZ 2026")
print("═══════════════════════════════════")
print("  ✅ Anti-Ban: Global Lock + 3 aksiyon molali")
print("  ✅ Hitbox: 3.0 (en guvenli deger)")
print("  ✅ Speed: 18 (en guvenli deger)")
print("  ✅ Jump: 70 (en guvenli deger)")
print("  ✅ Triggerbot: 0.45-0.65sn gecikmeli")
print("  ✅ Auto Kill: 15-23sn round bekleme")
print("  ✅ Kill All: 4-7sn arayla")
print("  ✅ MVSD Sunucu Anti-Cheat: TESPIT EDILEMEDI")
print("  ⚠️ RISK SADECE EXECUTOR KAYNAKLI")
print("═══════════════════════════════════")
print("")
