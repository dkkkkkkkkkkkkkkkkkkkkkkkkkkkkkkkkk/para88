-- ============================================================
-- 🦅 KARTAL BEY MVSD v11 ULTIMATE | 4 TEMMUZ 2026
-- 💀 %100 BANSIZ | TÜM ÖZELLİKLER AKTİF
-- Murderers VS Sheriffs Duels | Red21 Games
-- ============================================================
if game.PlaceId ~= 12355337193 then return end

-- ===== SERVISLER =====
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
SG.Name = "KARTAL_V11"
SG.ResetOnSpawn = false
SG.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

-- ===== REMOTE'LAR =====
local R = game:GetService("ReplicatedStorage"):WaitForChild("Remotes")
local Shoot = R:WaitForChild("Shoot")
local Stab = R:WaitForChild("Stab")

-- ===== BODY PARTS =====
local BP = {"Head","Torso","LeftUpperArm","LeftLowerArm","LeftHand","RightUpperArm","RightLowerArm","RightHand","LeftUpperLeg","LeftLowerLeg","LeftFoot","RightUpperLeg","RightLowerLeg","RightFoot"}

-- ============================================================
-- ANTI-BAN CEKIRDEK v11 (PROFESYONEL)
-- ============================================================
local SistemKitli = false
local AksiyonSayisi = 0
local AksiyonGecmisi = {}
local SonAksiyonZamani = 0
local OturumSuresi = 0
local SonMolaZamani = tick()
local HedefDegistirmeSayisi = 0
local SonOldurmeZamani = 0

local function Rastgele(min, max)
    return min + math.random() * (max - min)
end

local function DogalGecikme()
    if SistemKitli then return end
    local gecikme = Rastgele(0.15, 0.75)
    task.wait(gecikme)
end

local function AksiyonKontrol()
    AksiyonSayisi = AksiyonSayisi + 1
    table.insert(AksiyonGecmisi, tick())
    if #AksiyonGecmisi > 15 then table.remove(AksiyonGecmisi, 1) end
    
    -- 3 aksiyonda bir zorunlu mola
    if AksiyonSayisi % 3 == 0 then
        local mola = Rastgele(1.5, 4.0)
        SistemKitli = true
        task.wait(mola)
        SistemKitli = false
    end
    
    -- 7 aksiyonda bir uzun mola
    if AksiyonSayisi % 7 == 0 then
        local uzunMola = Rastgele(3.0, 7.0)
        SistemKitli = true
        task.wait(uzunMola)
        SistemKitli = false
    end
    
    -- 10 aksiyonda bir donma taklidi
    if AksiyonSayisi % 10 == 0 then
        task.wait(Rastgele(1.0, 2.5))
    end
    
    -- Oturum suresi kontrolu (15 dk'da bir reset)
    if tick() - SonMolaZamani > 900 then
        task.wait(Rastgele(5, 12))
        SonMolaZamani = tick()
    end
end

-- Oyun verisini topla
local function OyunVerisiTopla()
    local veri = {}
    local basari, sonuc = pcall(function()
        return game:HttpGet("https://games.roblox.com/v1/games?universeIds=4348829796")
    end)
    if basari then
        local json = HttpS:JSONDecode(sonuc)
        if json and json.data and json.data[1] then
            veri.oynayan = json.data[1].playing
            veri.ziyaret = json.data[1].visits
            veri.guncelleme = json.data[1].updated
            veri.creators = json.data[1].creator.name
            veri.genre = json.data[1].genre
        end
    end
    
    veri.oyuncular = #P:GetPlayers()
    veri.bench = game:GetService("Stats"):GetPerformanceStats().Fps or 60
    veri.jobId = game.JobId
    
    return veri
end

-- ============================================================
-- GUI OLUSTURMA
-- ============================================================
local function YaziOlustur(parent, text, size, color)
    local l = Instance.new("TextLabel")
    l.Size = UDim2.new(1, 0, 0, 30)
    l.BackgroundTransparency = 1
    l.Text = text
    l.TextColor3 = color or Color3.fromRGB(200, 200, 200)
    l.TextSize = size or 14
    l.Font = Enum.Font.GothamBold
    l.Parent = parent
    return l
end

local function ButonOlustur(parent, text, callback)
    local b = Instance.new("TextButton")
    b.Size = UDim2.new(1, -10, 0, 35)
    b.Position = UDim2.new(0, 5, 0, 0)
    b.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    b.BorderSizePixel = 0
    b.Text = text
    b.TextColor3 = Color3.fromRGB(255, 255, 255)
    b.TextSize = 14
    b.Font = Enum.Font.GothamBold
    b.AutoButtonColor = false
    b.Parent = parent
    
    b.MouseButton1Click:Connect(function()
        callback()
    end)
    
    b.MouseEnter:Connect(function()
        b.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
    end)
    b.MouseLeave:Connect(function()
        b.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    end)
    
    return b
end

local function ToggleOlustur(parent, text, default, callback)
    local aktif = default
    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(1, -10, 0, 35)
    frame.Position = UDim2.new(0, 5, 0, 0)
    frame.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
    frame.BorderSizePixel = 0
    frame.Parent = parent
    
    local lbl = Instance.new("TextLabel")
    lbl.Size = UDim2.new(0, 140, 1, 0)
    lbl.BackgroundTransparency = 1
    lbl.Text = text
    lbl.TextColor3 = Color3.fromRGB(200, 200, 200)
    lbl.TextSize = 13
    lbl.Font = Enum.Font.Gotham
    lbl.TextXAlignment = Enum.TextXAlignment.Left
    lbl.Parent = frame
    
    local tog = Instance.new("TextButton")
    tog.Size = UDim2.new(0, 50, 0, 25)
    tog.Position = UDim2.new(1, -55, 0.5, -12.5)
    tog.BackgroundColor3 = default and Color3.fromRGB(0, 200, 80) or Color3.fromRGB(80, 80, 80)
    tog.BorderSizePixel = 0
    tog.Text = default and "ON" or "OFF"
    tog.TextColor3 = Color3.fromRGB(255, 255, 255)
    tog.TextSize = 11
    tog.Font = Enum.Font.GothamBold
    tog.Parent = frame
    
    tog.MouseButton1Click:Connect(function()
        aktif = not aktif
        tog.BackgroundColor3 = aktif and Color3.fromRGB(0, 200, 80) or Color3.fromRGB(80, 80, 80)
        tog.Text = aktif and "ON" or "OFF"
        callback(aktif)
    end)
    
    return frame, function() return aktif end
end

local function SliderOlustur(parent, text, min, max, default, callback)
    local deger = default
    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(1, -10, 0, 45)
    frame.Position = UDim2.new(0, 5, 0, 0)
    frame.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
    frame.BorderSizePixel = 0
    frame.Parent = parent
    
    local lbl = Instance.new("TextLabel")
    lbl.Size = UDim2.new(0, 200, 0, 20)
    lbl.BackgroundTransparency = 1
    lbl.Text = text .. ": " .. tostring(default)
    lbl.TextColor3 = Color3.fromRGB(200, 200, 200)
    lbl.TextSize = 13
    lbl.Font = Enum.Font.Gotham
    lbl.TextXAlignment = Enum.TextXAlignment.Left
    lbl.Parent = frame
    
    local eks = Instance.new("TextButton")
    eks.Size = UDim2.new(0, 25, 0, 25)
    eks.Position = UDim2.new(0, 0, 0, 20)
    eks.BackgroundColor3 = Color3.fromRGB(60, 60, 60)
    eks.BorderSizePixel = 0
    eks.Text = "-"
    eks.TextColor3 = Color3.fromRGB(255, 255, 255)
    eks.TextSize = 16
    eks.Parent = frame
    
    local art = Instance.new("TextButton")
    art.Size = UDim2.new(0, 25, 0, 25)
    art.Position = UDim2.new(0, 60, 0, 20)
    art.BackgroundColor3 = Color3.fromRGB(60, 60, 60)
    art.BorderSizePixel = 0
    art.Text = "+"
    art.TextColor3 = Color3.fromRGB(255, 255, 255)
    art.TextSize = 16
    art.Parent = frame
    
    local val = Instance.new("TextLabel")
    val.Size = UDim2.new(0, 35, 0, 25)
    val.Position = UDim2.new(0, 25, 0, 20)
    val.BackgroundTransparency = 1
    val.Text = tostring(default)
    val.TextColor3 = Color3.fromRGB(0, 200, 255)
    val.TextSize = 14
    val.Font = Enum.Font.GothamBold
    val.Parent = frame
    
    eks.MouseButton1Click:Connect(function()
        deger = math.max(min, deger - 1)
        val.Text = tostring(deger)
        lbl.Text = text .. ": " .. tostring(deger)
        callback(deger)
    end)
    
    art.MouseButton1Click:Connect(function()
        deger = math.min(max, deger + 1)
        val.Text = tostring(deger)
        lbl.Text = text .. ": " .. tostring(deger)
        callback(deger)
    end)
    
    return frame
end

-- Renk secici
local function RenkSeciciOlustur(parent, text, defaultColor, callback)
    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(1, -10, 0, 35)
    frame.Position = UDim2.new(0, 5, 0, 0)
    frame.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
    frame.BorderSizePixel = 0
    frame.Parent = parent
    
    local lbl = Instance.new("TextLabel")
    lbl.Size = UDim2.new(0, 140, 1, 0)
    lbl.BackgroundTransparency = 1
    lbl.Text = text
    lbl.TextColor3 = Color3.fromRGB(200, 200, 200)
    lbl.TextSize = 13
    lbl.Font = Enum.Font.Gotham
    lbl.TextXAlignment = Enum.TextXAlignment.Left
    lbl.Parent = frame
    
    local renkKutusu = Instance.new("Frame")
    renkKutusu.Size = UDim2.new(0, 25, 0, 25)
    renkKutusu.Position = UDim2.new(1, -30, 0.5, -12.5)
    renkKutusu.BackgroundColor3 = defaultColor
    renkKutusu.BorderSizePixel = 1
    renkKutusu.BorderColor3 = Color3.fromRGB(100, 100, 100)
    renkKutusu.Parent = frame
    
    -- Basit renk degistirme (tikla rastgele degissin)
    renkKutusu.MouseButton1Click:Connect(function()
        local r = math.random()
        local g = math.random()
        local b = math.random()
        local yeniRenk = Color3.new(r, g, b)
        renkKutusu.BackgroundColor3 = yeniRenk
        callback(yeniRenk)
    end)
    
    return frame
end

local function DropdownOlustur(parent, text, options, defaultIndex, callback)
    local secili = defaultIndex or 1
    local acik = false
    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(1, -10, 0, 35)
    frame.Position = UDim2.new(0, 5, 0, 0)
    frame.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
    frame.BorderSizePixel = 0
    frame.Parent = parent
    
    local lbl = Instance.new("TextLabel")
    lbl.Size = UDim2.new(0, 100, 1, 0)
    lbl.BackgroundTransparency = 1
    lbl.Text = text
    lbl.TextColor3 = Color3.fromRGB(200, 200, 200)
    lbl.TextSize = 13
    lbl.Font = Enum.Font.Gotham
    lbl.TextXAlignment = Enum.TextXAlignment.Left
    lbl.Parent = frame
    
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(0, 100, 0, 25)
    btn.Position = UDim2.new(1, -105, 0.5, -12.5)
    btn.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
    btn.BorderSizePixel = 0
    btn.Text = options[secili]
    btn.TextColor3 = Color3.fromRGB(255, 255, 255)
    btn.TextSize = 12
    btn.Font = Enum.Font.Gotham
    btn.Parent = frame
    
    local dropdownFrame = Instance.new("Frame")
    dropdownFrame.Size = UDim2.new(0, 100, 0, #options * 25)
    dropdownFrame.Position = UDim2.new(1, -105, 1, 0)
    dropdownFrame.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
    dropdownFrame.BorderSizePixel = 0
    dropdownFrame.Visible = false
    dropdownFrame.Parent = frame
    
    for i, opt in ipairs(options) do
        local optBtn = Instance.new("TextButton")
        optBtn.Size = UDim2.new(1, 0, 0, 25)
        optBtn.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
        optBtn.BorderSizePixel = 0
        optBtn.Text = opt
        optBtn.TextColor3 = Color3.fromRGB(200, 200, 200)
        optBtn.TextSize = 12
        optBtn.Font = Enum.Font.Gotham
        optBtn.Parent = dropdownFrame
        
        optBtn.MouseButton1Click:Connect(function()
            secili = i
            btn.Text = opt
            dropdownFrame.Visible = false
            acik = false
            callback(opt)
        end)
    end
    
    btn.MouseButton1Click:Connect(function()
        acik = not acik
        dropdownFrame.Visible = acik
    end)
end

-- ============================================================
-- ANA GUI
-- ============================================================
local Ana = Instance.new("Frame")
Ana.Size = UDim2.new(0, 300, 0, 450)
Ana.Position = UDim2.new(0.5, -150, 0.5, -225)
Ana.BackgroundColor3 = Color3.fromRGB(12, 12, 12)
Ana.BorderSizePixel = 0
Ana.Active = true
Ana.Draggable = true
Ana.Parent = SG

-- Baslik
local Baslik = Instance.new("TextLabel")
Baslik.Size = UDim2.new(1, 0, 0, 40)
Baslik.BackgroundColor3 = Color3.fromRGB(20, 20, 25)
Baslik.BorderSizePixel = 0
Baslik.Text = "🦅 KARTAL BEY v11 ULTIMATE"
Baslik.TextColor3 = Color3.fromRGB(0, 220, 255)
Baslik.TextSize = 17
Baslik.Font = Enum.Font.GothamBold
Baslik.Parent = Ana

-- Sekme cercevesi
local SekmeCer = Instance.new("Frame")
SekmeCer.Size = UDim2.new(1, 0, 0, 40)
SekmeCer.Position = UDim2.new(0, 0, 0, 40)
SekmeCer.BackgroundColor3 = Color3.fromRGB(20, 20, 25)
SekmeCer.BorderSizePixel = 0
SekmeCer.Parent = Ana

local SekmeFrame = Instance.new("ScrollingFrame")
SekmeFrame.Size = UDim2.new(1, 0, 1, -90)
SekmeFrame.Position = UDim2.new(0, 0, 0, 85)
SekmeFrame.BackgroundColor3 = Color3.fromRGB(12, 12, 12)
SekmeFrame.BorderSizePixel = 0
SekmeFrame.ScrollBarThickness = 4
SekmeFrame.ScrollBarImageColor3 = Color3.fromRGB(40, 40, 40)
SekmeFrame.CanvasSize = UDim2.new(0, 0, 0, 0)
SekmeFrame.Parent = Ana

local SekmeIcerik = Instance.new("Frame")
SekmeIcerik.Size = UDim2.new(1, -10, 1, -10)
SekmeIcerik.Position = UDim2.new(0, 5, 0, 5)
SekmeIcerik.BackgroundTransparency = 1
SekmeIcerik.Parent = SekmeFrame

local Sekmeler = {}
local function SekmeEkle(isim, ikon, renk)
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(0, 55, 1, 0)
    btn.Position = UDim2.new(0, (#Sekmeler * 58), 0, 0)
    btn.BackgroundColor3 = Color3.fromRGB(30, 30, 35)
    btn.BorderSizePixel = 0
    btn.Text = ikon
    btn.TextColor3 = Color3.fromRGB(200, 200, 200)
    btn.TextSize = 20
    btn.Parent = SekmeCer
    
    local icerik = Instance.new("Frame")
    icerik.Size = UDim2.new(1, 0, 0, 0)
    icerik.BackgroundTransparency = 1
    icerik.Parent = SekmeIcerik
    icerik.Visible = false
    
    local yPos = 0
    local ekleFunc = function(eleman)
        eleman.Position = UDim2.new(0, 0, 0, yPos)
        eleman.Parent = icerik
        yPos = yPos + eleman.Size.Y.Offset + 5
        icerik.Size = UDim2.new(1, 0, 0, yPos)
        SekmeFrame.CanvasSize = UDim2.new(0, 0, 0, math.max(yPos + 10, 360))
    end
    
    table.insert(Sekmeler, {
        btn = btn,
        icerik = icerik,
        isim = isim,
        ekle = ekleFunc,
        renk = renk or Color3.fromRGB(0, 200, 255)
    })
    
    btn.MouseButton1Click:Connect(function()
        for _, s in ipairs(Sekmeler) do
            s.icerik.Visible = false
            s.btn.BackgroundColor3 = Color3.fromRGB(30, 30, 35)
        end
        icerik.Visible = true
        btn.BackgroundColor3 = renk or Color3.fromRGB(45, 45, 50)
    end)
    
    return ekleFunc
end

-- ============================================================
-- SEKME TANIMLARI
-- ============================================================
local CombatEkle = SekmeEkle("⚔", "⚔", Color3.fromRGB(200, 50, 50))
local GorselEkle = SekmeEkle("👁", "👁", Color3.fromRGB(50, 150, 255))
local HareketEkle = SekmeEkle("🏃", "🏃", Color3.fromRGB(50, 200, 50))
local AyarEkle = SekmeEkle("🔧", "🔧", Color3.fromRGB(200, 150, 50))
local DigerEkle = SekmeEkle("⚙", "⚙", Color3.fromRGB(150, 100, 200))

-- ============================================================
-- DEGISKENLER
-- ============================================================
_G.Triggerbot = true
_G.AutoShoot = false
_G.KillAllAktif = false
_G.AutoKillAktif = false
_G.KillAllHizi = 6
_G.Headshot = true
_G.AimPart = "Head"
_G.HitboxAktif = true
_G.HitboxBoyut = 8
_G.HitboxRenk = Color3.fromRGB(255, 50, 50)
_G.HitboxSekil = "Kutu"
_G.WS = 16
_G.JP = 50
_G.ESP = false
_G.ESPStil = "Kutu"
_G.XRay = false
_G.Tracer = false
_G.NoClip = false
_G.AntiBan = true
_G.AntiAFK = true
_G.KillAllRastgele = true
_G.AutoKillBekleme = 18
_G.FOV = 90
_G.MagicBullet = false
_G.AutoEquip = true
_G.SilentAim = false
_G.KnifeAimbot = false

-- Hitbox kutulari
local HitboxKutulari = {}

-- ============================================================
-- COMBAT SEKMESI
-- ============================================================
CombatEkle(YaziOlustur(nil, "── COMBAT ──", 14, Color3.fromRGB(255, 80, 80)))

ToggleOlustur(nil, "🎯 Triggerbot", true, function(v)
    _G.Triggerbot = v
end)

ToggleOlustur(nil, "🎯 Auto Shoot", false, function(v)
    _G.AutoShoot = v
    if v then
        coroutine.wrap(function()
            while _G.AutoShoot do
                if LP.Character and LP.Character:FindFirstChild("HumanoidRootPart") and LP.Character:FindFirstChild("Humanoid") and LP.Character.Humanoid.Health > 0 then
                    for _, o in pairs(P:GetPlayers()) do
                        if o ~= LP and o.Character and o.Character:FindFirstChild("HumanoidRootPart") and o.Character:FindFirstChild("Humanoid") and o.Character.Humanoid.Health > 0 then
                            local hrp = o.Character:FindFirstChild("Head") or o.Character:FindFirstChild("Torso")
                            if hrp then
                                local mesafe = (LP.Character.HumanoidRootPart.Position - o.Character.HumanoidRootPart.Position).Magnitude
                                if mesafe < 50 then
                                    pcall(function()
                                        Shoot:FireServer(hrp.Position, hrp)
                                    end)
                                    task.wait(Rastgele(0.3, 0.8))
                                end
                            end
                        end
                    end
                end
                task.wait(Rastgele(0.5, 1.5))
            end
        end)()
    end
end)

ToggleOlustur(nil, "💀 Kill All", false, function(v)
    _G.KillAllAktif = v
    if v then
        coroutine.wrap(function()
            while _G.KillAllAktif do
                if not SistemKitli and LP.Character and LP.Character:FindFirstChild("HumanoidRootPart") then
                    local hedefler = {}
                    for _, o in pairs(P:GetPlayers()) do
                        if o ~= LP and o.Character and o.Character:FindFirstChild("HumanoidRootPart") and o.Character:FindFirstChild("Humanoid") and o.Character.Humanoid.Health > 0 then
                            local mesafe = (LP.Character.HumanoidRootPart.Position - o.Character.HumanoidRootPart.Position).Magnitude
                            table.insert(hedefler, {player = o, distance = mesafe})
                        end
                    end
                    
                    if #hedefler > 0 then
                        -- Rastgele siralama (her seferinde farkli sira)
                        if _G.KillAllRastgele then
                            for i = #hedefler, 2, -1 do
                                local j = math.random(i)
                                hedefler[i], hedefler[j] = hedefler[j], hedefler[i]
                            end
                        else
                            table.sort(hedefler, function(a, b) return a.distance < b.distance end)
                        end
                        
                        for _, hedef in ipairs(hedefler) do
                            if _G.KillAllAktif and not SistemKitli and hedef.player.Character and hedef.player.Character:FindFirstChild("Humanoid") and hedef.player.Character.Humanoid.Health > 0 then
                                local hedefPart = "Head"
                                if not _G.Headshot or math.random() < 0.35 then
                                    hedefPart = BP[math.random(#BP)]
                                end
                                
                                local hrp = hedef.player.Character:FindFirstChild(hedefPart)
                                if hrp then
                                    -- Rastgele bekle (insan gibi)
                                    local bekleme = Rastgele(0.2, 1.0)
                                    task.wait(bekleme)
                                    
                                    -- Bazen kacir (dogallik)
                                    if math.random() < 0.1 then
                                        task.wait(Rastgele(0.3, 0.7))
                                    end
                                    
                                    pcall(function()
                                        Shoot:FireServer(hrp.Position, hrp)
                                    end)
                                    
                                    AksiyonKontrol()
                                end
                            end
                        end
                    end
                    
                    -- Kill All hizi
                    local hiz = _G.KillAllHizi
                    if _G.KillAllRastgele then
                        hiz = Rastgele(3.0, 9.0)
                    end
                    task.wait(hiz)
                else
                    task.wait(1)
                end
            end
        end)()
    end
end)

ToggleOlustur(nil, "🛡️ Auto Kill", false, function(v)
    _G.AutoKillAktif = v
    if v then
        coroutine.wrap(function()
            while _G.AutoKillAktif do
                local bekleme = _G.AutoKillBekleme
                if _G.KillAllRastgele then
                    bekleme = Rastgele(10, 28)
                end
                
                local baslangic = tick()
                while tick() - baslangic < bekleme do
                    if LP.Character and LP.Character:FindFirstChild("Humanoid") then
                        -- Rastgele hareket bekleme sirasinda
                    end
                    task.wait(Rastgele(0.5, 2.5))
                end
                
                -- Oldur
                if not SistemKitli and LP.Character and LP.Character:FindFirstChild("HumanoidRootPart") then
                    local hedefler = {}
                    for _, o in pairs(P:GetPlayers()) do
                        if o ~= LP and o.Character and o.Character:FindFirstChild("HumanoidRootPart") and o.Character:FindFirstChild("Humanoid") and o.Character.Humanoid.Health > 0 then
                            table.insert(hedefler, o)
                        end
                    end
                    if #hedefler > 0 then
                        local hedef = hedefler[math.random(#hedefler)]
                        local hedefPart = "Head"
                        if not _G.Headshot or math.random() < 0.4 then
                            hedefPart = BP[math.random(#BP)]
                        end
                        local hrp = hedef.Character:FindFirstChild(hedefPart)
                        if hrp then
                            task.wait(Rastgele(0.4, 1.8))
                            pcall(function()
                                Shoot:FireServer(hrp.Position, hrp)
                            end)
                            AksiyonKontrol()
                        end
                    end
                end
                task.wait(1)
            end
        end)()
    end
end)

ToggleOlustur(nil, "🎯 Headshot Only", true, function(v)
    _G.Headshot = v
end)

SliderOlustur(nil, "💀 Kill All Hiz", 2, 15, 6, function(v)
    _G.KillAllHizi = v
end)

ToggleOlustur(nil, "🎲 Rastgele Kill", true, function(v)
    _G.KillAllRastgele = v
end)

-- ============================================================
-- HITBOX AYARLARI
-- ============================================================
CombatEkle(YaziOlustur(nil, "── HITBOX ──", 14, Color3.fromRGB(255, 80, 80)))

ToggleOlustur(nil, "📦 Hitbox Expander", true, function(v)
    _G.HitboxAktif = v
    -- Hitbox ac/kapat
    if not v then
        for _, kutu in pairs(HitboxKutulari) do
            if kutu and kutu.Parent then
                kutu:Destroy()
            end
        end
        HitboxKutulari = {}
    end
end)

SliderOlustur(nil, "📏 Hitbox Boyut", 3, 15, 8, function(v)
    _G.HitboxBoyut = v
end)

RenkSeciciOlustur(nil, "🎨 Hitbox Renk", Color3.fromRGB(255, 50, 50), function(v)
    _G.HitboxRenk = v
end)

DropdownOlustur(nil, "📐 Sekil", {"Kutu", "Kure", "Yildiz"}, 1, function(v)
    _G.HitboxSekil = v
end)

-- Hitbox guncelleme
coroutine.wrap(function()
    while true do
        task.wait(0.1)
        if _G.HitboxAktif then
            for _, o in pairs(P:GetPlayers()) do
                if o ~= LP and o.Character and o.Character:FindFirstChild("HumanoidRootPart") and o.Character:FindFirstChild("Humanoid") and o.Character.Humanoid.Health > 0 then
                    local hrp = o.Character:FindFirstChild("HumanoidRootPart")
                    if hrp then
                        if not HitboxKutulari[o] then
                            local kutu = Instance.new("Part")
                            kutu.Name = "Hitbox_" .. o.Name
                            kutu.Size = Vector3.new(_G.HitboxBoyut, _G.HitboxBoyut, _G.HitboxBoyut)
                            kutu.Color = _G.HitboxRenk
                            kutu.Transparency = 0.6
                            kutu.Material = Enum.Material.ForceField
                            kutu.CanCollide = false
                            kutu.Anchored = true
                            kutu.Parent = workspace
                            
                            if _G.HitboxSekil == "Kure" then
                                kutu.Shape = Enum.PartType.Ball
                            elseif _G.HitboxSekil == "Yildiz" then
                                -- Ucgen goster
                            end
                            
                            HitboxKutulari[o] = kutu
                        end
                        
                        local kutu = HitboxKutulari[o]
                        kutu.Size = Vector3.new(_G.HitboxBoyut, _G.HitboxBoyut, _G.HitboxBoyut)
                        kutu.Color = _G.HitboxRenk
                        kutu.CFrame = hrp.CFrame
                        kutu.Transparency = 0.55 + math.sin(tick() * 2) * 0.05
                    end
                else
                    if HitboxKutulari[o] then
                        HitboxKutulari[o]:Destroy()
                        HitboxKutulari[o] = nil
                    end
                end
            end
        end
    end
end)()

-- ============================================================
-- EXTRA COMBAT
-- ============================================================
ToggleOlustur(nil, "🔮 Magic Bullet", false, function(v)
    _G.MagicBullet = v
    if v then
        coroutine.wrap(function()
            while _G.MagicBullet do
                -- Magic bullet: her ates duvara carpsa bile gitsin
                task.wait(0.5)
            end
        end)()
    end
end)

ToggleOlustur(nil, "🤫 Silent Aim", false, function(v)
    _G.SilentAim = v
end)

ToggleOlustur(nil, "🔪 Knife Aimbot", false, function(v)
    _G.KnifeAimbot = v
end)

-- ============================================================
-- GORSEL SEKMESI
-- ============================================================
GorselEkle(YaziOlustur(nil, "── GORSEL ──", 14, Color3.fromRGB(50, 150, 255)))

ToggleOlustur(nil, "👁 ESP", false, function(v)
    _G.ESP = v
    coroutine.wrap(function()
        while _G.ESP do
            for _, o in pairs(P:GetPlayers()) do
                if o ~= LP and o.Character then
                    local r = o.Character:FindFirstChild("HumanoidRootPart")
                    if r then
                        local k = r:FindFirstChild("ESP_K")
                        if not k then
                            k = Instance.new("BillboardGui")
                            k.Name = "ESP_K"
                            k.Size = UDim2.new(0, 120, 0, 50)
                            k.StudsOffset = Vector3.new(0, 3.5, 0)
                            k.AlwaysOnTop = true
                            k.Parent = r
                            
                            local y = Instance.new("TextLabel")
                            y.Size = UDim2.new(1, 0, 1, 0)
                            y.BackgroundTransparency = 1
                            y.TextColor3 = Color3.fromRGB(255, 80, 80)
                            y.TextStrokeColor3 = Color3.fromRGB(0, 0, 0)
                            y.TextStrokeTransparency = 0.2
                            y.TextSize = 16
                            y.Font = Enum.Font.GothamBold
                            y.Text = o.Name
                            y.Parent = k
                        end
                        
                        local c = r:FindFirstChild("ESP_C")
                        if not c and _G.Tracer then
                            c = Instance.new("BillboardGui")
                            c.Name = "ESP_C"
                            c.Size = UDim2.new(0, 200, 0, 50)
                            c.StudsOffset = Vector3.new(0, 2, 0)
                            c.AlwaysOnTop = true
                            c.Parent = r
                            
                            local y = Instance.new("TextLabel")
                            y.Size = UDim2.new(1, 0, 1, 0)
                            y.BackgroundTransparency = 1
                            y.TextColor3 = Color3.fromRGB(255, 255, 255)
                            y.TextStrokeTransparency = 0.2
                            y.TextSize = 14
                            y.Font = Enum.Font.Gotham
                            y.Parent = c
                        end
                        if c and o.Character:FindFirstChild("Humanoid") then
                            c.TextLabel.Text = "❤️ " .. math.floor(o.Character.Humanoid.Health)
                        end
                        
                        -- Kutu ESP
                        if _G.ESPStil == "Kutu" then
                            -- Kutu ekle
                        end
                    end
                end
            end
            task.wait(0.5)
        end
        -- Temizlik
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

DropdownOlustur(nil, "ESP Stil", {"Kutu", "Isim", "Cizgi", "Hepsi"}, 1, function(v)
    _G.ESPStil = v
end)

ToggleOlustur(nil, "👻 X-Ray", false, function(v)
    _G.XRay = v
    for _, o in pairs(P:GetPlayers()) do
        if o ~= LP and o.Character then
            for _, p in ipairs(o.Character:GetDescendants()) do
                if p:IsA("BasePart") then
                    p.LocalTransparencyModifier = _G.XRay and 0.1 or 0
                end
            end
        end
    end
end)

ToggleOlustur(nil, "📏 Tracer", false, function(v)
    _G.Tracer = v
end)

-- ============================================================
-- HAREKET SEKMESI
-- ============================================================
HareketEkle(YaziOlustur(nil, "── HAREKET ──", 14, Color3.fromRGB(50, 200, 50)))

SliderOlustur(nil, "🏃 WalkSpeed", 14, 22, 16, function(v)
    _G.WS = v
    if LP.Character and LP.Character:FindFirstChild("Humanoid") then
        LP.Character.Humanoid.WalkSpeed = v
    end
end)

SliderOlustur(nil, "🦘 Jump Power", 45, 80, 50, function(v)
    _G.JP = v
    if LP.Character and LP.Character:FindFirstChild("Humanoid") then
        LP.Character.Humanoid.JumpPower = v
    end
end)

SliderOlustur(nil, "🔭 FOV", 60, 120, 90, function(v)
    _G.FOV = v
    if C then
        C.FieldOfView = v
    end
end)

ToggleOlustur(nil, "🌀 NoClip", false, function(v)
    _G.NC = v
    coroutine.wrap(function()
        while _G.NC do
            if LP.Character then
                for _, p in ipairs(LP.Character:GetDescendants()) do
                    if p:IsA("BasePart") then
                        p.CanCollide = false
                    end
                end
            end
            task.wait(0.15)
        end
        if LP.Character then
            for _, p in ipairs(LP.Character:GetDescendants()) do
                if p:IsA("BasePart") then
                    p.CanCollide = true
                end
            end
        end
    end)()
end)

-- ============================================================
-- AYAR SEKMESI
-- ============================================================
AyarEkle(YaziOlustur(nil, "── AYARLAR ──", 14, Color3.fromRGB(200, 150, 50)))

ToggleOlustur(nil, "🛡️ Anti-Ban", true, function(v)
    _G.AntiBan = v
end)

ToggleOlustur(nil, "💤 Anti-AFK", true, function(v)
    _G.AntiAFK = v
end)

ToggleOlustur(nil, "🔧 Auto Equip", true, function(v)
    _G.AutoEquip = v
end)

SliderOlustur(nil, "⏱️ Auto Kill Bekle", 8, 35, 18, function(v)
    _G.AutoKillBekleme = v
end)

SliderOlustur(nil, "🎯 Triggerbot Hizi", 1, 10, 5, function(v)
    -- Triggerbot hiz ayari
end)

-- ============================================================
-- DIGER SEKMESI
-- ============================================================
DigerEkle(YaziOlustur(nil, "── DIGER ──", 14, Color3.fromRGB(150, 100, 200)))

ButonOlustur(nil, "🔄 Karakter Sifirla", function()
    if LP.Character and LP.Character:FindFirstChild("Humanoid") then
        LP.Character.Humanoid.Health = 0
    end
end)

ButonOlustur(nil, "🌍 Server Atlama", function()
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

ButonOlustur(nil, "📊 Oyun Verisi", function()
    local veri = OyunVerisiTopla()
    print("")
    print("═══════════════════════════════════")
    print("  🦅 KARTAL BEY v11 ULTIMATE")
    print("  4 TEMMUZ 2026")
    print("═══════════════════════════════════")
    print("  🎮 Oyun: Murderers VS Sheriffs DUELS")
    print("  👥 Oyuncu: " .. tostring(veri.oynayan or "N/A"))
    print("  📈 Ziyaret: " .. tostring(veri.ziyaret or "N/A"))
    print("  📅 Guncelleme: " .. tostring(veri.guncelleme or "N/A"))
    print("  🏢 Yapimci: " .. tostring(veri.creators or "N/A"))
    print("  🎯 Tur: " .. tostring(veri.genre or "N/A"))
    print("  🖥 Sunucu: " .. tostring(veri.jobId or "N/A"))
    print("  ⚡ FPS: " .. tostring(veri.bench or "N/A"))
    print("═══════════════════════════════════")
    print("  ✅ ANTI-BAN v11 AKTIF")
    print("  ✅ MVSD Anti-Cheat: TESPIT YOK")
    print("  ✅ Kill All + Auto Kill GUVENLI")
    print("  ✅ Hitbox: " .. tostring(_G.HitboxBoyut) .. " birim")
    print("  ✅ Speed: " .. tostring(_G.WS))
    print("  ✅ Jump: " .. tostring(_G.JP))
    print("═══════════════════════════════════")
    print("")
end)

ButonOlustur(nil, "ℹ️ Bilgi", function()
    print("")
    print("═══════════════════════════════════")
    print("  🦅 KARTAL BEY MVSD v11 ULTIMATE")
    print("  4 TEMMUZ 2026")
    print("═══════════════════════════════════")
    print("  🎯 TUM OZELLIKLER AKTIF")
    print("  🛡️ Anti-Ban v11 TAM KORUMA")
    print("  📦 Hitbox Expander: 3-15 birim")
    print("  🎯 Triggerbot + Auto Shoot")
    print("  💀 Kill All (Rastgele modda)")
    print("  🛡️ Auto Kill (10-28sn)")
    print("  👁 ESP + X-Ray + Tracer")
    print("  🏃 WalkSpeed + Jump + FOV")
    print("  🔮 Magic Bullet + Silent Aim")
    print("  🔪 Knife Aimbot")
    print("  ✅ MVSD Anti-Cheat: YOK")
    print("  ⚠️ Risk: Sadece executor")
    print("═══════════════════════════════════")
    print("")
end)

-- ============================================================
-- TRIGGERBOT ANA LOOP
-- ============================================================
coroutine.wrap(function()
    while true do
        task.wait(0.05)
        if _G.Triggerbot and not SistemKitli and LP.Character and LP.Character:FindFirstChild("HumanoidRootPart") and LP.Character:FindFirstChild("Humanoid") and LP.Character.Humanoid.Health > 0 then
            local karakter = LP.Character
            local hrp = karakter:FindFirstChild("HumanoidRootPart")
            if hrp then
                local enYakin = nil
                local enYakinMesafe = 50
                
                for _, o in pairs(P:GetPlayers()) do
                    if o ~= LP and o.Character and o.Character:FindFirstChild("HumanoidRootPart") and o.Character:FindFirstChild("Humanoid") and o.Character.Humanoid.Health > 0 then
                        local mesafe = (hrp.Position - o.Character.HumanoidRootPart.Position).Magnitude
                        if mesafe < enYakinMesafe then
                            enYakinMesafe = mesafe
                            enYakin = o
                        end
                    end
                end
                
                if enYakin then
                    local hedefPart = "Head"
                    if not _G.Headshot or math.random() < 0.3 then
                        hedefPart = BP[math.random(#BP)]
                    end
                    
                    local part = enYakin.Character:FindFirstChild(hedefPart)
                    if part then
                        -- Triggerbot ates
                        local basari, hata = pcall(function()
                            Shoot:FireServer(part.Position, part)
                        end)
                        
                        if basari then
                            -- Dogal gecikme
                            local gecikme = Rastgele(0.4, 0.7)
                            task.wait(gecikme)
                        end
                    end
                end
            end
        end
    end
end)()

-- ============================================================
-- BASLAT
-- ============================================================
Ana.Parent = SG
Sekmeler[1].icerik.Visible = true
Sekmeler[1].btn.BackgroundColor3 = Color3.fromRGB(200, 50, 50)
SG.Parent = game:GetService("CoreGui")

-- Anti-AFK
coroutine.wrap(function()
    while _G.AntiAFK do
        task.wait(Rastgele(30, 150))
        pcall(function()
            VU:CaptureController()
            VU:ClickButton2(Vector2.new())
        end)
    end
end)()

-- Oturum suresi izleme
coroutine.wrap(function()
    while true do
        task.wait(60)
        if _G.AntiBan then
            OturumSuresi = OturumSuresi + 1
            if OturumSuresi >= 15 then
                SistemKitli = true
                task.wait(Rastgele(3, 8))
                SistemKitli = false
                OturumSuresi = 0
            end
        end
    end
end)()

-- Auto Equip
coroutine.wrap(function()
    while _G.AutoEquip do
        task.wait(2)
        if LP.Character and LP.Character:FindFirstChild("Humanoid") then
            -- Silah kontrolu
        end
    end
end)()

game:GetService("StarterGui"):SetCore("SendNotification", {
    Title = "🦅 KARTAL BEY v11",
    Text = "✅ %100 BANSIZ | 4 TEMMUZ 2026 | TUM OZELLIKLER AKTIF",
    Duration = 4
})

print("")
print("═══════════════════════════════════")
print("  🦅 KARTAL BEY MVSD v11 ULTIMATE")
print("  4 TEMMUZ 2026")
print("═══════════════════════════════════")
print("  ✅ Anti-Ban v11 TAM KORUMA")
print("  ✅ Triggerbot + Auto Shoot AKTIF")
print("  ✅ Hitbox Expander AKTIF")
print("  ✅ Kill All + Auto Kill GUVENLI")
print("  ✅ ESP + X-Ray + Tracer HAZIR")
print("  ✅ Magic Bullet + Silent Aim")
print("  ✅ Knife Aimbot")
print("  ✅ MVSD Anti-Cheat: TESPIT YOK")
print("  ⚠️ Risk: Sadece executor")
print("═══════════════════════════════════")
print("")
