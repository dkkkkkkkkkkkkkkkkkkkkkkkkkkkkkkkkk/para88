-- ============================================================
-- DELTA PRO MVSD | KARTAL BEY
-- Sürüm 6.0 - SON | Tüm özellikler bansız
-- Murderers VS Sheriffs Duels
-- ============================================================

-- Oyun kontrolü
if game.PlaceId ~= 12355337193 then return end

-- Servisler
local P = game:GetService("Players")
local RS = game:GetService("RunService")
local UIS = game:GetService("UserInputService")
local VU = game:GetService("VirtualUser")
local LP = P.LocalPlayer
local M = LP:GetMouse()
local C = workspace.CurrentCamera
local SG = Instance.new("ScreenGui")
SG.Name = "KARTALBEY"; SG.ResetOnSpawn = false; SG.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

-- Remotes
local R = game:GetService("ReplicatedStorage"):WaitForChild("Remotes")
local Shoot = R:WaitForChild("Shoot")
local Stab = R:WaitForChild("Stab")

-- Body
local BP = {"Head","Torso","LeftUpperArm","LeftLowerArm","LeftHand","RightUpperArm","RightLowerArm","RightHand","LeftUpperLeg","LeftLowerLeg","LeftFoot","RightUpperLeg","RightLowerLeg","RightFoot"}

-- ===== ANTI-BAN ÇEKİRDEK =====
local lastShoot = 0; local shootCount = 0
local function AntiSpam()
    local now = tick()
    if now - lastShoot > 1 then shootCount = 0; lastShoot = now end
    shootCount = shootCount + 1
    if shootCount > 3 then task.wait(0.8 + math.random() * 0.5); shootCount = 0; lastShoot = tick() end
end

coroutine.wrap(function() while true do task.wait(150 + math.random() * 90) pcall(function() VU:CaptureController(); VU:ClickButton2(Vector2.new()) end) end end)()

local function rd(mn, mx) task.wait(mn + math.random() * (mx - mn)) end
local function rv() return Vector3.new(math.random()*2-1, math.random()*2-1, math.random()*2-1) end
local function rb(c) return c:FindFirstChild(BP[math.random(#BP)]) or c:FindFirstChild("HumanoidRootPart") end
local function isEnemy(m) local p = P:GetPlayerFromCharacter(m); return p and p ~= LP and p.Team ~= LP.Team end
local function isLive(c) return c and c:FindFirstChild("Humanoid") and c.Humanoid.Health > 0 end

local function getClosest()
    local c, cd = nil, math.huge
    for _, v in pairs(P:GetPlayers()) do
        if v ~= LP and isLive(v.Character) and isEnemy(v.Character) then
            local h = v.Character:FindFirstChild("HumanoidRootPart")
            if h then
                local p, on = C:WorldToViewportPoint(h.Position)
                if on then
                    local d = (Vector2.new(M.X, M.Y) - Vector2.new(p.X, p.Y)).Magnitude
                    if d < cd then c = v; cd = d end
                end
            end
        end
    end
    return c
end

local function getAll()
    local l = {}
    for _, v in pairs(P:GetPlayers()) do
        if v ~= LP and isLive(v.Character) and isEnemy(v.Character) then table.insert(l, v) end
    end
    for i = #l, 1, -1 do local j = math.random(1, i); l[i], l[j] = l[j], l[i] end
    return l
end

local function doShoot(c)
    if not Shoot or not c then return false end
    local p = rb(c); if not p then return false end
    AntiSpam(); Shoot:FireServer(rv(), rv(), p, rv()); return true
end

local function doStab(c)
    if not Stab or not c then return false end
    local h = c:FindFirstChild("HumanoidRootPart"); if not h then return false end
    AntiSpam(); Stab:FireServer(h); return true
end

-- ===== UI - KÜÇÜK BOYUT =====

local main = Instance.new("Frame")
main.Size = UDim2.new(0, 280, 0, 380)
main.Position = UDim2.new(0.5, -140, 0.5, -190)
main.BackgroundColor3 = Color3.fromRGB(8, 8, 8)
main.BackgroundTransparency = 0.1
main.BorderSizePixel = 0
main.Active = true
main.Draggable = true
local uc = Instance.new("UICorner", main); uc.CornerRadius = UDim.new(0, 8)
local us = Instance.new("UIStroke", main); us.Color = Color3.fromRGB(0, 180, 255); us.Thickness = 1.2; us.Transparency = 0.4

-- Baslik
local baslik = Instance.new("TextLabel")
baslik.Size = UDim2.new(1, 0, 0, 28)
baslik.BackgroundColor3 = Color3.fromRGB(0, 180, 255)
baslik.BackgroundTransparency = 0.85
baslik.Text = "KARTAL BEY | MVSD"
baslik.TextColor3 = Color3.fromRGB(0, 180, 255)
baslik.TextScaled = true; baslik.Font = Enum.Font.GothamBold
baslik.Parent = main
local buc = Instance.new("UICorner", baslik); buc.CornerRadius = UDim.new(0, 8)

local kapat = Instance.new("TextButton")
kapat.Size = UDim2.new(0, 20, 0, 20); kapat.Position = UDim2.new(1, -25, 0, 4)
kapat.BackgroundColor3 = Color3.fromRGB(255, 50, 50); kapat.BackgroundTransparency = 0.5
kapat.Text = "X"; kapat.TextColor3 = Color3.fromRGB(255,255,255); kapat.TextScaled = true; kapat.Font = Enum.Font.GothamBold; kapat.BorderSizePixel = 0
kapat.Parent = baslik
local kc = Instance.new("UICorner", kapat); kc.CornerRadius = UDim.new(0, 4)
kapat.MouseButton1Click:Connect(function() main.Visible = not main.Visible end)

-- Sekmeler
local tabFrame = Instance.new("Frame")
tabFrame.Size = UDim2.new(1, -10, 0, 28); tabFrame.Position = UDim2.new(0, 5, 0, 30)
tabFrame.BackgroundTransparency = 1; tabFrame.BorderSizePixel = 0; tabFrame.Parent = main

local tabs = {"C", "H", "E", "M", "X"}
local tabNames = {"Combat", "Hitbox", "ESP", "Move", "Misc"}
local tabIcons = {"⚔", "🎯", "👁", "🏃", "⚙"}
local currentTab = nil
local tabBtns = {}
local tabContents = {}

local function switchTab(n)
    if currentTab and tabContents[currentTab] then tabContents[currentTab].Visible = false end
    if currentTab and tabBtns[currentTab] then tabBtns[currentTab].BackgroundColor3 = Color3.fromRGB(20, 20, 20); tabBtns[currentTab].TextColor3 = Color3.fromRGB(120, 120, 120) end
    currentTab = n
    if tabContents[n] then tabContents[n].Visible = true end
    if tabBtns[n] then tabBtns[n].BackgroundColor3 = Color3.fromRGB(0, 180, 255); tabBtns[n].TextColor3 = Color3.fromRGB(255, 255, 255) end
end

for i = 1, 5 do
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(0, 50, 0, 24); btn.Position = UDim2.new(0, (i-1) * 54, 0, 2)
    btn.BackgroundColor3 = Color3.fromRGB(20, 20, 20); btn.Text = tabIcons[i]
    btn.TextColor3 = Color3.fromRGB(120, 120, 120); btn.TextScaled = true; btn.Font = Enum.Font.GothamSemibold; btn.BorderSizePixel = 0
    btn.Parent = tabFrame
    local tc = Instance.new("UICorner", btn); tc.CornerRadius = UDim.new(0, 4)
    btn.MouseButton1Click:Connect(function() switchTab(tabNames[i]) end)
    tabBtns[tabNames[i]] = btn
    
    local content = Instance.new("ScrollingFrame")
    content.Size = UDim2.new(1, -10, 1, -70); content.Position = UDim2.new(0, 5, 0, 62)
    content.BackgroundTransparency = 1; content.BorderSizePixel = 0
    content.ScrollBarThickness = 3; content.ScrollBarImageColor3 = Color3.fromRGB(0, 180, 255)
    content.CanvasSize = UDim2.new(0, 0, 0, 0); content.Parent = main; content.Visible = false
    tabContents[tabNames[i]] = content
end

-- Widget yardimci
local function addTog(tab, txt, cb)
    local f = tabContents[tab]; if not f then return end
    local y = f.CanvasSize.Y.Offset
    local fr = Instance.new("Frame")
    fr.Size = UDim2.new(1, -5, 0, 28); fr.Position = UDim2.new(0, 5, 0, y)
    fr.BackgroundColor3 = Color3.fromRGB(18, 18, 18); fr.BorderSizePixel = 0; fr.Parent = f
    local fc = Instance.new("UICorner", fr); fc.CornerRadius = UDim.new(0, 4)
    local lb = Instance.new("TextLabel")
    lb.Size = UDim2.new(1, -35, 1, 0); lb.Position = UDim2.new(0, 8, 0, 0)
    lb.BackgroundTransparency = 1; lb.Text = txt; lb.TextColor3 = Color3.fromRGB(200,200,200)
    lb.TextScaled = true; lb.TextXAlignment = Enum.TextXAlignment.Left; lb.Font = Enum.Font.GothamSemibold; lb.Parent = fr
    local bt = Instance.new("TextButton")
    bt.Size = UDim2.new(0, 22, 0, 22); bt.Position = UDim2.new(1, -28, 0, 3)
    bt.BackgroundColor3 = Color3.fromRGB(50, 50, 50); bt.Text = ""; bt.BorderSizePixel = 0; bt.Parent = fr
    local bc = Instance.new("UICorner", bt); bc.CornerRadius = UDim.new(0, 11)
    local s = false
    bt.MouseButton1Click:Connect(function() s = not s; bt.BackgroundColor3 = s and Color3.fromRGB(0, 180, 255) or Color3.fromRGB(50, 50, 50); if cb then cb(s) end end)
    f.CanvasSize = UDim2.new(0, 0, 0, y + 32)
end

local function addBtn(tab, txt, cb)
    local f = tabContents[tab]; if not f then return end
    local y = f.CanvasSize.Y.Offset
    local bt = Instance.new("TextButton")
    bt.Size = UDim2.new(1, -5, 0, 28); bt.Position = UDim2.new(0, 5, 0, y)
    bt.BackgroundColor3 = Color3.fromRGB(0, 180, 255); bt.BackgroundTransparency = 0.3
    bt.Text = txt; bt.TextColor3 = Color3.fromRGB(255,255,255); bt.TextScaled = true; bt.Font = Enum.Font.GothamBold; bt.BorderSizePixel = 0; bt.Parent = f
    local bc = Instance.new("UICorner", bt); bc.CornerRadius = UDim.new(0, 4)
    bt.MouseButton1Click:Connect(function()
        bt.BackgroundColor3 = Color3.fromRGB(255, 50, 50); task.wait(0.1)
        bt.BackgroundColor3 = Color3.fromRGB(0, 180, 255); if cb then cb() end
    end)
    f.CanvasSize = UDim2.new(0, 0, 0, y + 32)
end

local function addSld(tab, txt, mn, mx, def, cb)
    local f = tabContents[tab]; if not f then return end
    local y = f.CanvasSize.Y.Offset
    local fr = Instance.new("Frame")
    fr.Size = UDim2.new(1, -5, 0, 38); fr.Position = UDim2.new(0, 5, 0, y)
    fr.BackgroundColor3 = Color3.fromRGB(18, 18, 18); fr.BorderSizePixel = 0; fr.Parent = f
    local fc = Instance.new("UICorner", fr); fc.CornerRadius = UDim.new(0, 4)
    local lb = Instance.new("TextLabel")
    lb.Size = UDim2.new(1, -10, 0, 16); lb.Position = UDim2.new(0, 8, 0, 2)
    lb.BackgroundTransparency = 1; lb.Text = txt..": "..def; lb.TextColor3 = Color3.fromRGB(200,200,200)
    lb.TextScaled = true; lb.TextXAlignment = Enum.TextXAlignment.Left; lb.Font = Enum.Font.GothamSemibold; lb.Parent = fr
    
    local bg = Instance.new("Frame")
    bg.Size = UDim2.new(1, -16, 0, 5); bg.Position = UDim2.new(0, 8, 0, 22)
    bg.BackgroundColor3 = Color3.fromRGB(50, 50, 50); bg.BorderSizePixel = 0; bg.Parent = fr
    local bgc = Instance.new("UICorner", bg); bgc.CornerRadius = UDim.new(0, 2.5)
    local fill = Instance.new("Frame")
    fill.Size = UDim2.new((def-mn)/(mx-mn), 0, 1, 0)
    fill.BackgroundColor3 = Color3.fromRGB(0, 180, 255); fill.BorderSizePixel = 0; fill.Parent = bg
    local ffc = Instance.new("UICorner", fill); ffc.CornerRadius = UDim.new(0, 2.5)
    local drg = Instance.new("TextButton")
    drg.Size = UDim2.new(0, 12, 0, 12); drg.Position = UDim2.new((def-mn)/(mx-mn), -6, 0, -3.5)
    drg.BackgroundColor3 = Color3.fromRGB(0, 180, 255); drg.Text = ""; drg.BorderSizePixel = 0; drg.Parent = bg
    local dc = Instance.new("UICorner", drg); dc.CornerRadius = UDim.new(0, 6)
    
    local val = def; local dragging = false
    drg.InputBegan:Connect(function(i) if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then dragging = true end end)
    UIS.InputEnded:Connect(function(i) if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then dragging = false end end)
    UIS.InputChanged:Connect(function(i)
        if dragging and (i.UserInputType == Enum.UserInputType.MouseMovement or i.UserInputType == Enum.UserInputType.Touch) then
            local pct = math.clamp((UIS:GetMouseLocation().X - bg.AbsolutePosition.X) / bg.AbsoluteSize.X, 0, 1)
            val = math.floor(mn + (mx - mn) * pct)
            fill.Size = UDim2.new(pct, 0, 1, 0); drg.Position = UDim2.new(pct, -6, 0, -3.5)
            lb.Text = txt..": "..val; if cb then cb(val) end
        end
    end)
    f.CanvasSize = UDim2.new(0, 0, 0, y + 42)
end

-- ===== OZELLIKLER =====

-- COMBAT
addTog("Combat", "Silent Aim", function(v) _G.SilentAim = v end)
M.Button1Down:Connect(function()
    if _G.SilentAim then local t = getClosest(); if t and t.Character then doShoot(t.Character); rd(0.05, 0.15) end end
end)

addTog("Combat", "Triggerbot", function(v)
    _G.Trig = v
    if v then coroutine.wrap(function()
        while _G.Trig do local t = getClosest()
            if t and t.Character then local d = (t.Character.HumanoidRootPart.Position - LP.Character.HumanoidRootPart.Position).Magnitude
                if d < 60 then doShoot(t.Character); rd(0.3, 0.7) end end
            RS.RenderStepped:Wait() end
    end)() end
end)

addTog("Combat", "Auto Shoot", function(v)
    _G.AutoS = v
    if v then coroutine.wrap(function()
        while _G.AutoS do local t = getClosest()
            if t and t.Character then doShoot(t.Character); rd(0.15, 0.4) end
            task.wait(0.3) end
    end)() end
end)

addBtn("Combat", "Kill All [%100 Bansiz]", function()
    local e = getAll()
    for _, v in ipairs(e) do
        if isLive(v.Character) then
            if not doStab(v.Character) then doShoot(v.Character) end
            rd(2.5, 5.0) -- HER ÖLDÜRME ARASI 2.5-5 SANİYE BEKLE (BAN KORUMASI)
        end
    end
end)

addTog("Combat", "Auto Kill [Yavas]", function(v)
    _G.AutoK = v
    if v then coroutine.wrap(function()
        while _G.AutoK do
            task.wait(8 + math.random() * 5) -- İLK 8 SANİYE BEKLE (ROUND BASI)
            for _, v in ipairs(getAll()) do
                if isLive(v.Character) then doShoot(v.Character); rd(0.5, 1.5) end
            end
            rd(5.0, 10.0) -- TURLAR ARASI 5-10 SANİYE
        end
    end)() end
end)

-- HITBOX
_G.HBSize = 5
addTog("Hitbox", "Hitbox [Max 6]", function(v)
    _G.HB = v
    coroutine.wrap(function()
        while _G.HB do
            for _, v in pairs(P:GetPlayers()) do
                if v ~= LP and v.Character then
                    local h = v.Character:FindFirstChild("HumanoidRootPart")
                    if h then h.Size = Vector3.new(_G.HBSize, _G.HBSize, _G.HBSize); h.Transparency = 0.7 end
                end
            end
            task.wait(0.3)
        end
        for _, v in pairs(P:GetPlayers()) do
            if v ~= LP and v.Character then
                local h = v.Character:FindFirstChild("HumanoidRootPart")
                if h then h.Size = Vector3.new(2,2,1); h.Transparency = 1 end
            end
        end
    end)()
end)
addSld("Hitbox", "Size", 1, 6, 5, function(v) _G.HBSize = v end)

-- ESP
addTog("ESP", "ESP Box + Can", function(v)
    _G.ESP = v
    coroutine.wrap(function()
        while _G.ESP do
            for _, v in pairs(P:GetPlayers()) do
                if v ~= LP and v.Character then
                    local h = v.Character:FindFirstChild("HumanoidRootPart")
                    if h then
                        local bx = h:FindFirstChild("ESP_B")
                        if not bx then bx = Instance.new("BoxHandleAdornment", h); bx.Name = "ESP_B"; bx.Adornee = h; bx.AlwaysOnTop = true; bx.ZIndex = 10 end
                        bx.Size = Vector3.new(4,6,4); bx.Color3 = v.Team == LP.Team and Color3.fromRGB(0,255,0) or Color3.fromRGB(255,50,50)
                        bx.Transparency = 0.4; bx.Visible = true
                        local hp = h:FindFirstChild("ESP_C")
                        if not hp and v.Character:FindFirstChild("Humanoid") then
                            hp = Instance.new("BillboardGui", h); hp.Name = "ESP_C"
                            hp.Size = UDim2.new(0,80,0,16); hp.StudsOffset = Vector3.new(0,3.5,0); hp.AlwaysOnTop = true
                            local l = Instance.new("TextLabel", hp); l.Size = UDim2.new(1,0,1,0); l.BackgroundTransparency = 1
                            l.TextScaled = true; l.Font = Enum.Font.GothamBold; l.TextColor3 = Color3.fromRGB(255,255,255); l.TextStrokeTransparency = 0.3
                        end
                        if hp and hp:IsA("BillboardGui") then
                            local l = hp:FindFirstChildOfClass("TextLabel")
                            if l and v.Character:FindFirstChild("Humanoid") then l.Text = v.Name.." ["..math.floor(v.Character.Humanoid.Health).."HP]" end
                        end
                    end
                end
            end
            task.wait(0.3)
        end
        for _, v in pairs(P:GetPlayers()) do
            if v.Character then
                local h = v.Character:FindFirstChild("HumanoidRootPart")
                if h then local b = h:FindFirstChild("ESP_B"); if b then b:Destroy() end; local c = h:FindFirstChild("ESP_C"); if c then c:Destroy() end end
            end
        end
    end)()
end)

addTog("ESP", "X-Ray", function(v)
    for _, v in pairs(P:GetPlayers()) do
        if v ~= LP and v.Character then for _, p in ipairs(v.Character:GetDescendants()) do if p:IsA("BasePart") then p.LocalTransparencyModifier = v and 0.2 or 0 end end end
    end
end)

-- MOVEMENT
_G.WS = 16
addSld("Move", "WalkSpeed [Max 22]", 16, 22, 16, function(v)
    _G.WS = v; if LP.Character and LP.Character:FindFirstChild("Humanoid") then LP.Character.Humanoid.WalkSpeed = v end
end)

_G.JP = 50
addSld("Move", "Jump", 50, 100, 50, function(v)
    _G.JP = v; if LP.Character and LP.Character:FindFirstChild("Humanoid") then LP.Character.Humanoid.JumpPower = v end
end)

addTog("Move", "NoClip", function(v)
    _G.NC = v
    coroutine.wrap(function()
        while _G.NC do
            if LP.Character then for _, p in ipairs(LP.Character:GetDescendants()) do if p:IsA("BasePart") then p.CanCollide = false end end end
            task.wait(0.1)
        end
        if LP.Character then for _, p in ipairs(LP.Character:GetDescendants()) do if p:IsA("BasePart") then p.CanCollide = true end end end
    end)()
end)

-- MISC
addBtn("Misc", "Karakter Sifirla", function()
    if LP.Character and LP.Character:FindFirstChild("Humanoid") then LP.Character.Humanoid.Health = 0 end
end)

addBtn("Misc", "Server Atlama", function()
    local ts = game:GetService("TeleportService")
    local res = game:HttpGet("https://games.roblox.com/v1/games/"..game.PlaceId.."/servers/Public?limit=100")
    local d = game:GetService("HttpService"):JSONDecode(res)
    for _, s in ipairs(d.data) do if s.id ~= game.JobId and s.playing < s.maxPlayers then ts:TeleportToPlaceInstance(game.PlaceId, s.id, LP); return end end
end)

addBtn("Misc", "Bilgi", function()
    print("=== KARTAL BEY MVSD ===")
    print("Shoot: "..tostring(Shoot)); print("Stab: "..tostring(Stab))
    print("Anti-Ban: AKTIF (Spam korumali, yavas mod)")
    print("========================")
end)

-- Baslat
main.Parent = SG
switchTab("Combat")
SG.Parent = game:GetService("CoreGui")

-- Bildirim
StarterGui = game:GetService("StarterGui")
StarterGui:SetCore("SendNotification", {Title = "KARTAL BEY", Text = "MVSD Hazir! Bansiz oyna.", Duration = 3})

print("=== KARTAL BEY MVSD ===")
print("Boyut kucultuldu, ban korumasi eklendi")
print("Kill All arasi 2.5-5 saniye bekleme")
print("Auto Kill ilk 8 saniye bekleme")
print("Hitbox max 6, Speed max 22")
print("========================")
