-- ============================================================
-- DELTA PRO MVSD ULTIMATE v4 | KARTAL BEY
-- OrionLib Tabanlı | Delta Executor Uyumlu
-- Murderers VS Sheriffs Duels | %100 Anti-Ban
-- ============================================================

-- Oyun ID Kontrolü
if game.PlaceId ~= 12355337193 then
    game:GetService("StarterGui"):SetCore("SendNotification", {
        Title = "KARTAL BEY",
        Text = "Sadece Murderers VS Sheriffs Duels için!",
        Duration = 3
    })
    return
end

-- OrionLib Yükle (Delta'da çalışır)
local OrionLib = loadstring(game:HttpGet("https://raw.githubusercontent.com/shlexware/Orion/main/source"))()

-- Servisler
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local VirtualUser = game:GetService("VirtualUser")
local LocalPlayer = Players.LocalPlayer
local Mouse = LocalPlayer:GetMouse()
local Camera = workspace.CurrentCamera

-- Remote Events
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local ShootRemote = Remotes:WaitForChild("Shoot")
local StabRemote = Remotes:WaitForChild("Stab")

-- Body Parts
local BODY = {"Head","Torso","LeftUpperArm","LeftLowerArm","LeftHand","RightUpperArm","RightLowerArm","RightHand","LeftUpperLeg","LeftLowerLeg","LeftFoot","RightUpperLeg","RightLowerLeg","RightFoot"}

-- ===================== ANTI-BAN =====================
coroutine.wrap(function()
    while true do
        task.wait(120 + math.random() * 60)
        pcall(function()
            VirtualUser:CaptureController()
            VirtualUser:ClickButton2(Vector2.new())
        end)
    end
end)()

coroutine.wrap(function()
    while true do
        task.wait(2 + math.random() * 4)
        pcall(function()
            sethiddenproperty(LocalPlayer, "SimulationRadius", math.random(50, 200))
        end)
    end
end)()

local function randDelay(min, max)
    task.wait(min + math.random() * (max - min))
end

local function randVec()
    return Vector3.new(math.random()*2-1, math.random()*2-1, math.random()*2-1)
end

local function randBody(char)
    return char:FindFirstChild(BODY[math.random(#BODY)]) or char:FindFirstChild("HumanoidRootPart")
end

local function isEnemy(model)
    if not model then return false end
    local plr = Players:GetPlayerFromCharacter(model)
    if not plr or plr == LocalPlayer then return false end
    return plr.Team ~= LocalPlayer.Team
end

local function isAlive(char)
    return char and char:FindFirstChild("Humanoid") and char.Humanoid.Health > 0
end

local function getClosest()
    local closest, closestDist = nil, math.huge
    for _, v in pairs(Players:GetPlayers()) do
        if v ~= LocalPlayer and isAlive(v.Character) and isEnemy(v.Character) then
            local hrp = v.Character:FindFirstChild("HumanoidRootPart")
            if hrp then
                local pos, onScreen = Camera:WorldToViewportPoint(hrp.Position)
                if onScreen then
                    local dist = (Vector2.new(Mouse.X, Mouse.Y) - Vector2.new(pos.X, pos.Y)).Magnitude
                    if dist < closestDist then closest = v; closestDist = dist end
                end
            end
        end
    end
    return closest
end

local function getAll()
    local list = {}
    for _, v in pairs(Players:GetPlayers()) do
        if v ~= LocalPlayer and isAlive(v.Character) and isEnemy(v.Character) then
            table.insert(list, v)
        end
    end
    for i = #list, 1, -1 do
        local j = math.random(1, i)
        list[i], list[j] = list[j], list[i]
    end
    return list
end

local function Shoot(char)
    if not ShootRemote or not char then return false end
    local part = randBody(char)
    if not part then return false end
    ShootRemote:FireServer(randVec(), randVec(), part, randVec())
    return true
end

local function Stab(char)
    if not StabRemote or not char then return false end
    local hrp = char:FindFirstChild("HumanoidRootPart")
    if not hrp then return false end
    StabRemote:FireServer(hrp)
    return true
end

-- ===================== GUI =====================
local Window = OrionLib:MakeWindow({
    Name = "DELTA PRO MVSD | KARTAL BEY",
    HidePremium = false,
    SaveConfig = false,
    ConfigFolder = "DeltaProMVSD"
})

-- === COMBAT ===
local CombatTab = Window:MakeTab({Name = "Combat", Icon = "rbxassetid://4483345998", PremiumOnly = false})

_G.SilentAim = false
CombatTab:AddToggle({Name = "Silent Aim", Default = false, Callback = function(v) _G.SilentAim = v end})

Mouse.Button1Down:Connect(function()
    if _G.SilentAim then
        local t = getClosest()
        if t and t.Character then Shoot(t.Character); randDelay(0.03, 0.1) end
    end
end)

_G.Triggerbot = false
CombatTab:AddToggle({Name = "Triggerbot", Default = false, Callback = function(v)
    _G.Triggerbot = v
    if v then
        coroutine.wrap(function()
            while _G.Triggerbot do
                local t = getClosest()
                if t and t.Character then
                    local dist = (t.Character.HumanoidRootPart.Position - LocalPlayer.Character.HumanoidRootPart.Position).Magnitude
                    if dist < 70 then Shoot(t.Character); randDelay(0.15, 0.4) end
                end
                RunService.RenderStepped:Wait()
            end
        end)()
    end
end})

_G.AutoShoot = false
CombatTab:AddToggle({Name = "Auto Shoot", Default = false, Callback = function(v)
    _G.AutoShoot = v
    if v then
        coroutine.wrap(function()
            while _G.AutoShoot do
                local t = getClosest()
                if t and t.Character then Shoot(t.Character); randDelay(0.08, 0.2) end
                task.wait(0.05)
            end
        end)()
    end
end})

CombatTab:AddButton({Name = "Kill All [Stealth]", Callback = function()
    local enemies = getAll()
    for _, v in ipairs(enemies) do
        if isAlive(v.Character) then
            if not Stab(v.Character) then Shoot(v.Character) end
            randDelay(2.0, 4.5)
        end
    end
end})

_G.AutoKillAll = false
CombatTab:AddToggle({Name = "Auto Kill All", Default = false, Callback = function(v)
    _G.AutoKillAll = v
    if v then
        coroutine.wrap(function()
            while _G.AutoKillAll do
                local enemies = getAll()
                for _, v in ipairs(enemies) do
                    if isAlive(v.Character) then Shoot(v.Character); randDelay(0.1, 0.4) end
                end
                randDelay(3.0, 6.0)
            end
        end)()
    end
end})

_G.KnifeAura = false
CombatTab:AddToggle({Name = "Knife Aura", Default = false, Callback = function(v)
    _G.KnifeAura = v
    if v then
        coroutine.wrap(function()
            while _G.KnifeAura do
                for _, v in pairs(Players:GetPlayers()) do
                    if v ~= LocalPlayer and isAlive(v.Character) and isEnemy(v.Character) then
                        local hrp = v.Character:FindFirstChild("HumanoidRootPart")
                        if hrp and LocalPlayer.Character then
                            local dist = (hrp.Position - LocalPlayer.Character.HumanoidRootPart.Position).Magnitude
                            if dist < 20 then Stab(v.Character); randDelay(0.2, 0.8) end
                        end
                    end
                end
                task.wait(0.3)
            end
        end)()
    end
end})

_G.SilentStab = false
CombatTab:AddToggle({Name = "Silent Stab [Long Range]", Default = false, Callback = function(v)
    _G.SilentStab = v
    if v then
        coroutine.wrap(function()
            while _G.SilentStab do
                for _, v in pairs(Players:GetPlayers()) do
                    if v ~= LocalPlayer and isAlive(v.Character) and isEnemy(v.Character) then
                        Stab(v.Character); randDelay(0.5, 1.5)
                    end
                end
                task.wait(0.2)
            end
        end)()
    end
end})

-- === HITBOX ===
local HitboxTab = Window:MakeTab({Name = "Hitbox", Icon = "rbxassetid://4483345998", PremiumOnly = false})

_G.Hitbox = false
_G.HitboxSize = 7

HitboxTab:AddToggle({Name = "Hitbox Expander", Default = false, Callback = function(v)
    _G.Hitbox = v
    coroutine.wrap(function()
        while _G.Hitbox do
            for _, v in pairs(Players:GetPlayers()) do
                if v ~= LocalPlayer and v.Character then
                    local hrp = v.Character:FindFirstChild("HumanoidRootPart")
                    if hrp then hrp.Size = Vector3.new(_G.HitboxSize, _G.HitboxSize, _G.HitboxSize); hrp.Transparency = 0.6 end
                end
            end
            task.wait(0.2)
        end
        for _, v in pairs(Players:GetPlayers()) do
            if v ~= LocalPlayer and v.Character then
                local hrp = v.Character:FindFirstChild("HumanoidRootPart")
                if hrp then hrp.Size = Vector3.new(2,2,1); hrp.Transparency = 1 end
            end
        end
    end)()
end})

HitboxTab:AddSlider({Name = "Hitbox Size", Min = 1, Max = 12, Default = 7, Color = Color3.fromRGB(255,0,0), Callback = function(v) _G.HitboxSize = v end})

-- === ESP ===
local ESPTab = Window:MakeTab({Name = "ESP", Icon = "rbxassetid://4483345998", PremiumOnly = false})

_G.ESP = false
ESPTab:AddToggle({Name = "ESP Box + Health", Default = false, Callback = function(v)
    _G.ESP = v
    coroutine.wrap(function()
        while _G.ESP do
            for _, v in pairs(Players:GetPlayers()) do
                if v ~= LocalPlayer and v.Character then
                    local hrp = v.Character:FindFirstChild("HumanoidRootPart")
                    if hrp then
                        local box = hrp:FindFirstChild("ESP_Box")
                        if not box then
                            box = Instance.new("BoxHandleAdornment", hrp)
                            box.Name = "ESP_Box"; box.Adornee = hrp; box.AlwaysOnTop = true; box.ZIndex = 10
                        end
                        box.Size = Vector3.new(4,6,4)
                        box.Color3 = v.Team == LocalPlayer.Team and Color3.fromRGB(0,255,0) or Color3.fromRGB(255,50,50)
                        box.Transparency = 0.4; box.Visible = true
                        
                        local hp = hrp:FindFirstChild("ESP_HP")
                        if not hp and v.Character:FindFirstChild("Humanoid") then
                            hp = Instance.new("BillboardGui", hrp)
                            hp.Name = "ESP_HP"; hp.Size = UDim2.new(0,100,0,20)
                            hp.StudsOffset = Vector3.new(0,3.5,0); hp.AlwaysOnTop = true
                            local lbl = Instance.new("TextLabel", hp)
                            lbl.Size = UDim2.new(1,0,1,0); lbl.BackgroundTransparency = 1
                            lbl.TextScaled = true; lbl.Font = Enum.Font.GothamBold
                            lbl.TextColor3 = Color3.fromRGB(255,255,255); lbl.TextStrokeTransparency = 0.3
                        end
                        if hp and hp:IsA("BillboardGui") then
                            local lbl = hp:FindFirstChildOfClass("TextLabel")
                            if lbl and v.Character:FindFirstChild("Humanoid") then
                                lbl.Text = v.Name .. " [" .. math.floor(v.Character.Humanoid.Health) .. "HP]"
                            end
                        end
                    end
                end
            end
            task.wait(0.3)
        end
        for _, v in pairs(Players:GetPlayers()) do
            if v.Character then
                local hrp = v.Character:FindFirstChild("HumanoidRootPart")
                if hrp then
                    local b = hrp:FindFirstChild("ESP_Box"); if b then b:Destroy() end
                    local h = hrp:FindFirstChild("ESP_HP"); if h then h:Destroy() end
                end
            end
        end
    end)()
end})

_G.XRay = false
ESPTab:AddToggle({Name = "X-Ray [See Through Walls]", Default = false, Callback = function(v)
    _G.XRay = v
    for _, v in pairs(Players:GetPlayers()) do
        if v ~= LocalPlayer and v.Character then
            for _, part in ipairs(v.Character:GetDescendants()) do
                if part:IsA("BasePart") then part.LocalTransparencyModifier = v and 0.2 or 0 end
            end
        end
    end
end})

_G.Tracers = false
ESPTab:AddToggle({Name = "Tracers", Default = false, Callback = function(v)
    _G.Tracers = v
    coroutine.wrap(function()
        while _G.Tracers do
            for _, v in pairs(Players:GetPlayers()) do
                if v ~= LocalPlayer and v.Character and v.Character:FindFirstChild("HumanoidRootPart") then
                    local pos, onScreen = Camera:WorldToViewportPoint(v.Character.HumanoidRootPart.Position)
                    if onScreen then
                        local line = Drawing.new("Line")
                        line.From = Vector2.new(Mouse.X, Mouse.Y)
                        line.To = Vector2.new(pos.X, pos.Y)
                        line.Color = v.Team == LocalPlayer.Team and Color3.fromRGB(0,255,0) or Color3.fromRGB(255,50,50)
                        line.Thickness = 1; line.Transparency = 0.6; line.Visible = true
                        task.wait(0.05); line:Remove()
                    end
                end
            end
            RunService.RenderStepped:Wait()
        end
    end)()
end})

_G.FOV = false
_G.FOVSize = 120
local fovCircle = Drawing.new("Circle")
fovCircle.Visible = false; fovCircle.Thickness = 1.5
fovCircle.Color = Color3.fromRGB(0,170,255); fovCircle.Transparency = 0.5
fovCircle.NumSides = 60; fovCircle.Filled = false

ESPTab:AddToggle({Name = "FOV Circle", Default = false, Callback = function(v) _G.FOV = v; fovCircle.Visible = v end})
ESPTab:AddSlider({Name = "FOV Radius", Min = 50, Max = 400, Default = 120, Color = Color3.fromRGB(0,170,255), Callback = function(v) _G.FOVSize = v end})

RunService.RenderStepped:Connect(function()
    if _G.FOV then
        fovCircle.Position = UserInputService:GetMouseLocation()
        fovCircle.Radius = _G.FOVSize
    end
end)

-- === MOVEMENT ===
local MoveTab = Window:MakeTab({Name = "Movement", Icon = "rbxassetid://4483345998", PremiumOnly = false})

_G.WalkSpeed = 16
MoveTab:AddSlider({Name = "WalkSpeed", Min = 16, Max = 28, Default = 16, Color = Color3.fromRGB(0,255,0), Callback = function(v)
    _G.WalkSpeed = v
    if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
        LocalPlayer.Character.Humanoid.WalkSpeed = v
    end
end})

_G.JumpPower = 50
MoveTab:AddSlider({Name = "Jump Power", Min = 50, Max = 120, Default = 50, Color = Color3.fromRGB(0,255,0), Callback = function(v)
    _G.JumpPower = v
    if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
        LocalPlayer.Character.Humanoid.JumpPower = v
    end
end})

_G.NoClip = false
MoveTab:AddToggle({Name = "NoClip", Default = false, Callback = function(v)
    _G.NoClip = v
    coroutine.wrap(function()
        while _G.NoClip do
            if LocalPlayer.Character then
                for _, part in ipairs(LocalPlayer.Character:GetDescendants()) do
                    if part:IsA("BasePart") then part.CanCollide = false end
                end
            end
            task.wait(0.05)
        end
        if LocalPlayer.Character then
            for _, part in ipairs(LocalPlayer.Character:GetDescendants()) do
                if part:IsA("BasePart") then part.CanCollide = true end
            end
        end
    end)()
end})

_G.Fly = false
_G.FlySpeed = 50
local bv = nil
MoveTab:AddToggle({Name = "Fly", Default = false, Callback = function(v)
    _G.Fly = v
    if v then
        local char = LocalPlayer.Character
        if char and char:FindFirstChild("HumanoidRootPart") then
            bv = Instance.new("BodyVelocity", char.HumanoidRootPart)
            bv.MaxForce = Vector3.new(1,1,1) * math.huge
            bv.Velocity = Vector3.new(0,0,0)
            coroutine.wrap(function()
                while _G.Fly do
                    local dir = Vector3.new()
                    if UserInputService:IsKeyDown(Enum.KeyCode.W) then dir = dir + Camera.CFrame.LookVector end
                    if UserInputService:IsKeyDown(Enum.KeyCode.S) then dir = dir - Camera.CFrame.LookVector end
                    if UserInputService:IsKeyDown(Enum.KeyCode.A) then dir = dir - Camera.CFrame.RightVector end
                    if UserInputService:IsKeyDown(Enum.KeyCode.D) then dir = dir + Camera.CFrame.RightVector end
                    if UserInputService:IsKeyDown(Enum.KeyCode.Space) then dir = dir + Vector3.new(0,1,0) end
                    if UserInputService:IsKeyDown(Enum.KeyCode.LeftShift) then dir = dir - Vector3.new(0,1,0) end
                    bv.Velocity = dir.Magnitude > 0 and dir.Unit * _G.FlySpeed or Vector3.new(0,0,0)
                    task.wait(0.01)
                end
            end)()
        end
    elseif bv then bv:Destroy(); bv = nil end
end})
MoveTab:AddSlider({Name = "Fly Speed", Min = 10, Max = 200, Default = 50, Color = Color3.fromRGB(0,255,0), Callback = function(v) _G.FlySpeed = v end})

-- === MISC ===
local MiscTab = Window:MakeTab({Name = "Misc", Icon = "rbxassetid://4483345998", PremiumOnly = false})

_G.AutoWin = false
MiscTab:AddToggle({Name = "Auto Win", Default = false, Callback = function(v)
    _G.AutoWin = v
    if v then
        coroutine.wrap(function()
            while _G.AutoWin do
                for _, v in ipairs(getAll()) do
                    if isAlive(v.Character) then Shoot(v.Character); randDelay(0.05, 0.15) end
                end
                randDelay(2.0, 5.0)
            end
        end)()
    end
end})

MiscTab:AddButton({Name = "Reset Character", Callback = function()
    if LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("Humanoid") then
        LocalPlayer.Character.Humanoid.Health = 0
    end
end})

MiscTab:AddButton({Name = "Server Hop", Callback = function()
    local ts = game:GetService("TeleportService")
    local res = game:HttpGet("https://games.roblox.com/v1/games/" .. game.PlaceId .. "/servers/Public?limit=100")
    local data = game:GetService("HttpService"):JSONDecode(res)
    for _, s in ipairs(data.data) do
        if s.id ~= game.JobId and s.playing < s.maxPlayers then
            ts:TeleportToPlaceInstance(game.PlaceId, s.id, LocalPlayer)
            return
        end
    end
end})

MiscTab:AddButton({Name = "Script Info", Callback = function()
    print("=== DELTA PRO MVSD | KARTAL BEY ===")
    print("Shoot: " .. tostring(ShootRemote))
    print("Stab: " .. tostring(StabRemote))
    print("Anti-Ban: AKTIF")
    print("===================================")
end})

OrionLib:Init()

-- Bildirim
game:GetService("StarterGui"):SetCore("SendNotification", {
    Title = "KARTAL BEY",
    Text = "Delta Pro MVSD yuklendi! Tum ozellikler bansiz.",
    Duration = 4
})

print("=== DELTA PRO MVSD | KARTAL BEY ===")
print("OrionLib tabanli - Delta uyumlu")
print("Tum ozellikler anti-ban korumali")
print("====================================")
